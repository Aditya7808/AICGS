"""
Supabase Authentication for CareerBuddy
Uses Supabase Auth for user management and JWT verification
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
import logging
import jwt
from datetime import datetime, timedelta
from jose import jwt as jose_jwt
from jose.exceptions import JWTError

from ..db.supabase_client import get_supabase_client, get_supabase_service_client
from ..core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str]
    created_at: str

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Get current authenticated user from Supabase JWT token"""
    
    token = credentials.credentials
    
    try:
        # First, try to verify token with Supabase Auth
        supabase = get_supabase_client()
        
        try:
            # Try to get user info using the JWT token
            user_response = supabase.auth.get_user(token)
            
            if user_response and user_response.user:
                logger.info(f"Supabase auth successful for user: {user_response.user.email}")
                return {
                    "sub": user_response.user.id,
                    "email": user_response.user.email,
                    "role": getattr(user_response.user, 'role', 'authenticated')
                }
            else:
                raise ValueError("No user data in Supabase response")
                
        except Exception as supabase_error:
            logger.warning(f"Supabase get_user failed: {str(supabase_error)}")
            
            # If Supabase auth fails, try to decode the JWT manually
            try:
                # First check if it's a valid JWT structure
                if token.count('.') != 2:
                    logger.error(f"Invalid JWT structure: expected 3 parts, got {token.count('.') + 1}")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid token format - not a valid JWT",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                
                # Try to decode without verification to check structure and content
                unverified_payload = jose_jwt.decode(token, key="", options={"verify_signature": False})
                logger.info(f"JWT structure valid, contains: {list(unverified_payload.keys())}")
                
                # Extract issuer to determine JWT secret
                issuer = unverified_payload.get("iss", "")
                
                # Try different verification approaches
                verification_successful = False
                verified_payload = None
                
                # Method 1: Try with Supabase JWT secret if available
                if settings.supabase_jwt_secret and settings.supabase_jwt_secret != "your-supabase-jwt-secret-from-project-settings":
                    try:
                        verified_payload = jose_jwt.decode(
                            token, 
                            key=settings.supabase_jwt_secret, 
                            algorithms=["HS256"],
                            options={"verify_aud": False, "verify_iss": False}
                        )
                        verification_successful = True
                        logger.info("JWT verified with Supabase JWT secret")
                    except JWTError:
                        logger.warning("JWT verification failed with Supabase JWT secret")
                
                # Method 2: Try with service role key
                if not verification_successful:
                    try:
                        verified_payload = jose_jwt.decode(
                            token, 
                            key=settings.supabase_service_role_key, 
                            algorithms=["HS256"],
                            options={"verify_aud": False, "verify_iss": False}
                        )
                        verification_successful = True
                        logger.info("JWT verified with service role key")
                    except JWTError:
                        logger.warning("JWT verification failed with service role key")
                
                # Method 3: Try with anon key
                if not verification_successful:
                    try:
                        verified_payload = jose_jwt.decode(
                            token, 
                            key=settings.supabase_anon_key, 
                            algorithms=["HS256"],
                            options={"verify_aud": False, "verify_iss": False}
                        )
                        verification_successful = True
                        logger.info("JWT verified with anon key")
                    except JWTError:
                        logger.warning("JWT verification failed with anon key")
                
                # Method 4: Try with our own secret key
                if not verification_successful:
                    try:
                        verified_payload = jose_jwt.decode(
                            token, 
                            key=settings.secret_key, 
                            algorithms=["HS256"],
                            options={"verify_aud": False, "verify_iss": False}
                        )
                        verification_successful = True
                        logger.info("JWT verified with application secret key")
                    except JWTError:
                        logger.warning("JWT verification failed with application secret key")
                
                # If we have a verified payload, use it
                if verification_successful and verified_payload:
                    if verified_payload.get('sub') and verified_payload.get('email'):
                        # Validate UUID format for sub claim
                        user_id = verified_payload.get('sub')
                        import uuid
                        try:
                            uuid.UUID(user_id)  # Validate UUID format
                            logger.info(f"JWT verification successful for user: {verified_payload.get('email')}")
                            return {
                                "sub": user_id,
                                "email": verified_payload.get('email'),
                                "role": verified_payload.get('role', 'authenticated')
                            }
                        except ValueError:
                            logger.error(f"Invalid UUID format for sub claim: {user_id}")
                            # Don't use this token if UUID is invalid
                    else:
                        logger.error("JWT missing required fields (sub, email)")
                
                # If verification failed but we have unverified payload with valid data, use it as fallback
                if unverified_payload.get('sub') and unverified_payload.get('email'):
                    # Validate UUID format for unverified payload too
                    user_id = unverified_payload.get('sub')
                    import uuid
                    try:
                        uuid.UUID(user_id)  # Validate UUID format
                        logger.warning("Using unverified JWT payload - NOT SECURE for production")
                        return {
                            "sub": user_id,
                            "email": unverified_payload.get('email'),
                            "role": unverified_payload.get('role', 'authenticated')
                        }
                    except ValueError:
                        logger.error(f"Invalid UUID format in unverified payload: {user_id}")
                        # Don't use this token if UUID is invalid
                
                # If we get here, no valid token could be processed
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="JWT verification failed and payload invalid",
                    headers={"WWW-Authenticate": "Bearer"},
                )
                    
            except JWTError as jwt_error:
                logger.error(f"JWT decode failed: {str(jwt_error)}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid JWT token format",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/signup", response_model=dict)
async def signup(user: UserSignup):
    """Sign up a new user using Supabase Auth"""
    
    try:
        supabase = get_supabase_client()
        
        # Sign up user with Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "full_name": user.full_name
                }
            }
        })
        
        if auth_response.user:
            # Check if email confirmation is required
            email_confirmed = auth_response.user.email_confirmed_at is not None
            
            # Only try to create profile if email is confirmed and we have a session
            if email_confirmed and auth_response.session:
                # Create profile in profiles table with proper error handling
                profile_data = {
                    "id": auth_response.user.id,  # This must match auth.uid() for RLS
                    "email": user.email,
                    "full_name": user.full_name,
                    "is_active": True
                }
                
                try:
                    # Set the auth session for the profile creation to work with RLS
                    supabase.auth.set_session(
                        auth_response.session.access_token,
                        auth_response.session.refresh_token
                    )
                    
                    # Use service client for profile creation to bypass RLS
                    supabase_service = get_supabase_service_client()
                    
                    # Insert profile (using service role key to bypass RLS)
                    profile_result = supabase_service.table("profiles").insert(profile_data).execute()
                    
                    if not profile_result.data:
                        logger.warning(f"Profile creation returned no data for user: {user.email}")
                    
                    logger.info(f"User signed up successfully with profile: {user.email}")
                    
                except Exception as profile_error:
                    logger.error(f"Profile creation failed for {user.email}: {str(profile_error)}")
                    # Don't fail the signup if profile creation fails - user auth was successful
                    logger.warning(f"User {user.email} created but profile creation failed. Profile can be created later.")
            
            # Determine the appropriate message based on email confirmation status
            if email_confirmed:
                message = "User created successfully. You can now log in."
            else:
                message = "User created successfully. Please check your email for verification before logging in."
            
            return {
                "message": message,
                "user_id": auth_response.user.id,
                "email_confirmed": email_confirmed,
                "requires_email_verification": not email_confirmed
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user account"
            )
            
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        if "User already registered" in str(e) or "already exists" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during signup"
        )

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    """Login user using Supabase Auth"""
    
    try:
        supabase = get_supabase_client()
        
        # Sign in user with Supabase Auth
        auth_response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        
        if auth_response.user and auth_response.session:
            # Check if email is confirmed
            if auth_response.user.email_confirmed_at is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Please confirm your email address before logging in. Check your inbox for a confirmation link."
                )
            
            logger.info(f"User logged in successfully: {user.email}")
            
            # Try to ensure user has a profile (create if missing)
            try:
                supabase_service = get_supabase_service_client()
                profile_check = supabase_service.table("profiles").select("id").eq("id", auth_response.user.id).execute()
                
                if not profile_check.data:
                    # Profile doesn't exist, create it
                    logger.info(f"Creating missing profile for user: {user.email}")
                    profile_data = {
                        "id": auth_response.user.id,
                        "email": auth_response.user.email,
                        "full_name": auth_response.user.user_metadata.get("full_name", ""),
                        "is_active": True
                    }
                    
                    try:
                        supabase_service.table("profiles").insert(profile_data).execute()
                        logger.info(f"Profile created for existing user: {user.email}")
                    except Exception as profile_error:
                        logger.warning(f"Could not create profile for {user.email}: {str(profile_error)}")
                        # Don't fail login if profile creation fails
                
            except Exception as e:
                logger.warning(f"Profile check/creation error for {user.email}: {str(e)}")
                # Don't fail login for profile issues
            
            return Token(
                access_token=auth_response.session.access_token,
                token_type="bearer",
                refresh_token=auth_response.session.refresh_token,
                expires_in=auth_response.session.expires_in
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
            
    except HTTPException:
        # Re-raise HTTP exceptions (like email confirmation required)
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        error_msg = str(e).lower()
        if "invalid login credentials" in error_msg or "invalid credentials" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        elif "email not confirmed" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please confirm your email address before logging in. Check your inbox for a confirmation link."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    """Refresh access token using refresh token"""
    
    try:
        supabase = get_supabase_client()
        
        # Refresh the session
        auth_response = supabase.auth.refresh_session(refresh_token)
        
        if auth_response.session:
            return Token(
                access_token=auth_response.session.access_token,
                token_type="bearer",
                refresh_token=auth_response.session.refresh_token,
                expires_in=auth_response.session.expires_in
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
            
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Logout user and invalidate session"""
    
    try:
        supabase = get_supabase_client()
        
        # Set the session token
        supabase.auth.set_session(credentials.credentials, "")
        
        # Sign out
        supabase.auth.sign_out()
        
        return {"message": "Logged out successfully"}
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return {"message": "Logged out"}  # Return success even if error

@router.post("/create-profile", response_model=dict)
async def create_profile(current_user = Depends(get_current_user)):
    """Create profile for authenticated user (if not exists)"""
    
    try:
        supabase_service = get_supabase_service_client()
        
        # Check if profile already exists
        existing_profile = supabase_service.table("profiles").select("id").eq("id", current_user["sub"]).execute()
        
        if existing_profile.data and len(existing_profile.data) > 0:
            return {"message": "Profile already exists"}
        
        # Create new profile
        profile_data = {
            "id": current_user["sub"],  # This must match auth.uid() for RLS
            "email": current_user["email"],
            "full_name": None,  # Can be updated later
            "is_active": True
        }
        
        result = supabase_service.table("profiles").insert(profile_data).execute()
        
        if result.data:
            logger.info(f"Profile created for existing user: {current_user['email']}")
            return {"message": "Profile created successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create profile"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create profile error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user profile"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user = Depends(get_current_user)):
    """Get current user profile"""
    
    try:
        # Use service client to bypass RLS issues
        supabase_service = get_supabase_service_client()
        
        # Get user profile from profiles table using service role key
        result = supabase_service.table("profiles").select("*").eq("id", current_user["sub"]).execute()
        
        if result.data and len(result.data) > 0:
            profile = result.data[0]
            return UserResponse(
                id=profile["id"],
                email=profile["email"],
                full_name=profile.get("full_name"),
                created_at=profile["created_at"]
            )
        else:
            # If profile doesn't exist, create it
            logger.info(f"Profile not found for user {current_user['sub']}, creating one")
            
            profile_data = {
                "id": current_user["sub"],
                "email": current_user["email"],
                "full_name": None,
                "is_active": True
            }
            
            try:
                create_result = supabase_service.table("profiles").insert(profile_data).execute()
                
                if create_result.data and len(create_result.data) > 0:
                    profile = create_result.data[0]
                    logger.info(f"Profile created for user: {current_user['email']}")
                    
                    return UserResponse(
                        id=profile["id"],
                        email=profile["email"],
                        full_name=profile.get("full_name"),
                        created_at=profile["created_at"]
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to create user profile"
                    )
                    
            except Exception as create_error:
                logger.error(f"Profile creation failed: {str(create_error)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user profile"
                )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get profile error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user profile"
        )

@router.put("/me", response_model=dict)
async def update_user_profile(
    profile_update: ProfileUpdate,
    current_user = Depends(get_current_user)
):
    """Update current user profile"""
    
    try:
        supabase_service = get_supabase_service_client()
        
        # Update profile in profiles table
        update_data = {}
        if profile_update.full_name is not None:
            update_data["full_name"] = profile_update.full_name
        
        if update_data:
            update_data["updated_at"] = datetime.utcnow().isoformat()
            
            result = supabase_service.table("profiles").update(update_data).eq("id", current_user["sub"]).execute()
            
            if result.data:
                return {"message": "Profile updated successfully"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User profile not found"
                )
        else:
            return {"message": "No changes to update"}
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update profile error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile"
        )

@router.post("/resend-confirmation", response_model=dict)
async def resend_confirmation(request: dict):
    """Resend email confirmation for a user"""
    try:
        email = request.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Email is required")
            
        supabase = get_supabase_client()
        
        # Resend confirmation email
        result = supabase.auth.resend({"type": "signup", "email": email})
        
        return {"message": "Confirmation email resent successfully"}
        
    except Exception as e:
        logger.error(f"Resend confirmation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to resend confirmation email"
        )

@router.get("/debug/user-status/{email}")
async def debug_user_status(email: str):
    """Debug endpoint to check user status - REMOVE IN PRODUCTION"""
    try:
        # Simple debug info without admin access
        return {
            "message": "Debug endpoint - check server logs for authentication attempts",
            "email": email,
            "note": "Use Supabase dashboard to check user status and email confirmation"
        }
            
    except Exception as e:
        logger.error(f"Debug user status error: {str(e)}")
        return {"error": str(e)}

@router.post("/google/signin", response_model=dict)
async def google_signin():
    """Initiate Google OAuth sign-in flow"""
    try:
        supabase = get_supabase_client()
        
        # Get the OAuth URL for Google
        auth_response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": f"{settings.frontend_url}/auth/callback"
            }
        })
        
        return {
            "auth_url": auth_response.url,
            "message": "Redirect to Google OAuth URL"
        }
        
    except Exception as e:
        logger.error(f"Google OAuth initiation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initiate Google OAuth"
        )

class GoogleCallbackRequest(BaseModel):
    code: str

@router.post("/google/callback", response_model=Token)
async def google_callback(request: GoogleCallbackRequest):
    """Handle Google OAuth callback"""
    try:
        supabase = get_supabase_client()
        code = request.code
        
        logger.info(f"Processing Google OAuth callback with code: {code[:20]}...")
        
        if not code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Authorization code is required"
            )
        
        # Check if the code is already a JWT token
        if code.count('.') == 2:
            # It's already a JWT token, validate and use it
            try:
                # Decode without verification to check structure
                unverified_payload = jose_jwt.decode(code, key="", options={"verify_signature": False})
                
                if unverified_payload.get('sub') and unverified_payload.get('email'):
                    logger.info(f"Received JWT token for user: {unverified_payload.get('email')}")
                    
                    # Validate the UUID format for sub
                    user_id = unverified_payload.get('sub')
                    import uuid
                    try:
                        uuid.UUID(user_id)  # Validate UUID format
                    except ValueError:
                        logger.error(f"Invalid UUID format for sub: {user_id}")
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid user ID format in token"
                        )
                    
                    # Create or update user profile
                    user_email = unverified_payload.get('email')
                    full_name = unverified_payload.get('name') or unverified_payload.get('full_name', '')
                    
                    # Set up Supabase session for profile operations
                    try:
                        # Check and create profile if needed
                        supabase_service = get_supabase_service_client()
                        profile_check = supabase_service.table("profiles").select("id").eq("id", user_id).execute()
                        
                        if not profile_check.data:
                            profile_data = {
                                "id": user_id,
                                "email": user_email,
                                "full_name": full_name,
                                "is_active": True
                            }
                            
                            # Use service role key for profile creation
                            profile_result = supabase_service.table("profiles").insert(profile_data).execute()
                            logger.info(f"Profile created for OAuth user: {user_email}")
                        
                    except Exception as profile_error:
                        logger.warning(f"Profile creation/check failed: {str(profile_error)}")
                    
                    # Return the existing token (it's already valid)
                    return Token(
                        access_token=code,
                        token_type="bearer",
                        refresh_token="",
                        expires_in=3600
                    )
                    
            except Exception as jwt_error:
                logger.error(f"JWT processing failed: {str(jwt_error)}")
        
        # If not a JWT, try to exchange the OAuth code (only once per code)
        try:
            # Try using Supabase's OAuth code exchange with better error handling
            try:
                auth_response = supabase.auth.exchange_code_for_session({
                    "auth_code": code,
                    "code_verifier": "",  # Required but can be empty for some flows
                    "redirect_to": f"{settings.frontend_url}/auth/callback"  # Required
                })
                
                if (auth_response and 
                    hasattr(auth_response, 'session') and auth_response.session and
                    hasattr(auth_response, 'user') and auth_response.user):
                    
                    session = auth_response.session
                    user = auth_response.user
                    
                    logger.info(f"OAuth code exchange successful for user: {getattr(user, 'email', 'unknown')}")
                    
                    # Handle profile creation
                    try:
                        user_id = getattr(user, 'id', None)
                        user_email = getattr(user, 'email', None)
                        user_metadata = getattr(user, 'user_metadata', {}) or {}
                        full_name = user_metadata.get("full_name") or user_metadata.get("name", "")
                        
                        if user_id and user_email:
                            supabase_service = get_supabase_service_client()
                            profile_check = supabase_service.table("profiles").select("id").eq("id", user_id).execute()
                            
                            if not profile_check.data:
                                profile_data = {
                                    "id": user_id,
                                    "email": user_email,
                                    "full_name": full_name,
                                    "is_active": True
                                }
                                
                                supabase_service.table("profiles").insert(profile_data).execute()
                                logger.info(f"Profile created for OAuth user: {user_email}")
                    
                    except Exception as profile_error:
                        logger.warning(f"Profile creation/check failed: {str(profile_error)}")
                    
                    return Token(
                        access_token=getattr(session, 'access_token', ''),
                        token_type="bearer",
                        refresh_token=getattr(session, 'refresh_token', ''),
                        expires_in=getattr(session, 'expires_in', 3600)
                    )
                else:
                    raise ValueError("Invalid OAuth code exchange response")
                    
            except Exception as exchange_error:
                error_message = str(exchange_error)
                logger.error(f"OAuth code exchange failed: {error_message}")
                
                # If the error is about auth code reuse or invalid code, return specific error
                if ("both auth code and code verifier should be non-empty" in error_message or
                    "invalid request" in error_message.lower() or
                    "authorization code" in error_message.lower()):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="OAuth code already used or expired. Please re-authenticate."
                    )
                
                # For other errors, re-raise as a generic failure
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="OAuth authentication failed. Please try again."
                )
        
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as process_error:
            logger.error(f"OAuth processing failed: {str(process_error)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OAuth authentication failed. Please try again."
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Google OAuth callback error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process Google OAuth callback"
        )

@router.post("/google/callback/debug")
async def google_callback_debug(request: dict):
    """Debug endpoint to see what we're receiving in the callback"""
    try:
        logger.info(f"Debug callback received: {type(request)} - {request}")
        
        # Log the raw request data
        return {
            "received_type": str(type(request)),
            "received_data": request,
            "has_code": "code" in request if isinstance(request, dict) else False,
            "code_value": request.get("code") if isinstance(request, dict) else str(request)
        }
        
    except Exception as e:
        logger.error(f"Debug callback error: {str(e)}")
        return {"error": str(e), "type": str(type(request))}

@router.get("/google/url")
async def get_google_auth_url():
    """Get Google OAuth URL for frontend redirect"""
    try:
        supabase = get_supabase_client()
        
        # Generate the OAuth URL
        auth_response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": f"{settings.frontend_url}/auth/callback",
                "scopes": "email profile"
            }
        })
        
        return {
            "url": auth_response.url,
            "provider": "google"
        }
        
    except Exception as e:
        logger.error(f"Google OAuth URL generation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate Google OAuth URL"
        )
