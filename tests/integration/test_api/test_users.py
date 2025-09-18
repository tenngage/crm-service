import pytest


class TestUserEndpoints:
    @pytest.mark.asyncio
    async def test_register_user_success(self, get_test_db):
        from src.services.user_services import register
        from src.schemas.user_schemas import UserRegister

        user_data = UserRegister(
            email="email123@gmail.com",
            username="user123",
            password="password123",
        )

        result = await register(get_test_db, user_data)

        assert result.email == user_data.email
        assert result.username == user_data.username

        from sqlalchemy import select
        from src.models.user import User

        db_result = await get_test_db.execute(select(User))
        users = db_result.scalars().all()
        assert len(users) == 1
        assert users[0].email == user_data.email
        assert users[0].username == user_data.username
