from app.infra.db.pg import engine, AsyncSessionLocal
from app.infra.db.models.base import Base
from app.infra.db.models.user_model import User
from app.core.security import hash_password
from app.core.config import settings
from sqlalchemy.future import select


async def create_initial_admin():
    # 1️⃣ Создаём таблицы (если их нет) через engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2️⃣ Проверяем, есть ли админ
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.role == "admin")
        )
        admin = result.scalar_one_or_none()
        if not admin:
            new_admin = User(
                id="jesus_christ",
                hashed_password=hash_password(settings.ROOT_USR_PASS),
                role="admin",
                is_active=True
            )
            session.add(new_admin)
            await session.commit()
            print("Initial admin created")
