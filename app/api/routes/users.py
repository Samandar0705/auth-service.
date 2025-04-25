from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserOut, UserBase

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: UserOut = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserOut)
async def update_user_me(
    user_in: UserBase,
    current_user: UserOut = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).filter(User.id == current_user.id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.email = user_in.email
    await db.commit()
    await db.refresh(user)
    return UserOut.from_orm(user)

@router.get("/", response_model=list[UserOut])
async def read_users(
    current_user: UserOut = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [UserOut.from_orm(user) for user in users]

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: UserOut = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    await db.execute(delete(User).filter(User.id == user_id))
    await db.commit()