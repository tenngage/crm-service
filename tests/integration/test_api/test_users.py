import pytest


class TestUserEndpoints:
    @pytest.mark.asyncio
    async def test_register_user_success(
        self,
        get_test_db,
        test_user_data,
        register_test_user,
    ):
        # Registering user for tests
        result = register_test_user

        assert result.email == test_user_data["email"]
        assert result.username == test_user_data["username"]

        from sqlalchemy import select
        from src.models.user import User

        # Check if user in db matches test user
        db_result = await get_test_db.execute(select(User))
        users = db_result.scalars().all()
        assert len(users) == 1
        assert users[0].email == test_user_data["email"]
        assert users[0].username == test_user_data["username"]

    @pytest.mark.asyncio
    async def test_login_user_success(
        self,
        get_test_db,
        test_user_data,
    ):
        from src.services.user_services import login
        from fastapi.security import OAuth2PasswordRequestForm

        # Mocking form_data
        form_data = OAuth2PasswordRequestForm(
            username=test_user_data["username"],
            password=test_user_data["password"],
            scope=""
        )

        # Trying to login
        result = await login(form_data, get_test_db)
        assert result.access_token
        assert result.token_type == "bearer"
