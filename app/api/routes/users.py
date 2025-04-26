from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from app.api.deps import get_current_user, require_permissions
from app.db.session import get_db
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserOut, UserBase
from typing import List

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

@router.get("/", response_model=List[UserOut])
async def read_users(
    current_user: UserOut = Depends(require_permissions(["read"])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [UserOut.from_orm(user) for user in users]

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: UserOut = Depends(require_permissions(["delete"])),
    db: AsyncSession = Depends(get_db)
):
    await db.execute(delete(User).filter(User.id == user_id))
    await db.commit()

@router.put("/{user_id}/role", response_model=UserOut)
async def update_user_role(
    user_id: int,
    role_id: int,
    current_user: UserOut = Depends(require_permissions(["admin"])),
    db: AsyncSession = Depends(get_db)
):
    # Foydalanuvchini topish
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Rolni topish
    result = await db.execute(select(Role).filter(Role.id == role_id))
    role = result.scalars().first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Foydalanuvchi rolini yangilash
    await db.execute(update(User).filter(User.id == user_id).values(role_id=role_id))
    await db.commit()
    await db.refresh(user)
    return UserOut.from_orm(user)