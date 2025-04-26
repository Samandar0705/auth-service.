from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import require_permissions
from app.db.session import get_db
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleOut
from app.schemas.user import UserOut

router = APIRouter(prefix="/roles", tags=["roles"])

@router.post("/", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_in: RoleCreate,
    current_user: UserOut = Depends(require_permissions(["admin"])),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Role).filter(Role.name == role_in.name))
    existing_role = result.scalars().first()
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role already exists"
        )

    new_role = Role(name=role_in.name, permissions=role_in.permissions)
    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)
    return RoleOut.from_orm(new_role)