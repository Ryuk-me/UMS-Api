from fastapi import HTTPException, status

USER_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found"
)
SOMETHING_WRONG_WITH_UMS_SERVER = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="UMS Server Down"
)

CREDENTIALS_NOT_VALID = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Incorrect Registration Number or Password.",
)

USER_IS_BANNED = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You have been banned from using our services.",
)

TIME_TABLE_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Time table not found."
)

MAKEUP_CLASS_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="No makeup class available"
)

LEAVE_SLIP_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Leave Slip Not Found"
)

LPU_LIVE_SEARCH_ERROR = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Something went wrong while searching for the user",
)
