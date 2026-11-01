from app.models.entities import User


class UserService:
    def __init__(self):
        self.__users: list[User] = []

    def create(self, id: int, name: str, email: str, role: str, state: str = 'ACTIVO') -> User:
        if self.find(id) is not None:
            raise ValueError('Ya existe un usuario con ese ID')
        user = User(id, name, email, role, state)
        self.__users.append(user)
        return user

    def list(self) -> list[User]:
        return list(self.__users)

    def find(self, id: int) -> User | None:
        return next((u for u in self.__users if u.id == id), None)

    def update(self, id: int, name: str, email: str, role: str, state: str) -> User:
        user = self.find(id)
        if user is None:
            raise ValueError('Usuario no encontrado')
        user.update(name, email, role, state)
        return user
