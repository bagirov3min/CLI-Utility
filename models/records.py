from crud.records import Text


class TextModel:
    """Операционный модуль для работы с текстом"""

    def __init__(self):
        self.text_db = Text()

    def add(self, user_id: int, text: str) -> None:
        """Функция добавления текста в таблицу"""
        check = self.text_db.add_text(user_id, text)
        if check:
            print('Текст успешно добавлен!')

    def update(self, user_id: int, text: str) -> None:
        """Функция обновления текста в таблице"""
        check = self.text_db.update_text(user_id, text)
        if check:
            print('Текст успешно обновлен!')
        else:
            print('Записи под таким номером не существует!')

    def delete(self, user_id: int) -> None:
        """Функция удаления текста из таблицы"""
        check = self.text_db.delete_text(user_id)
        if check:
            print('Запись удалена!')
        else:
            print('Записи под таким номером не существует!')

    def delete_all(self, user_id: int) -> None:
        """Функция удаления всего текста с этим user_id"""
        check = self.text_db.delete_all(user_id)
        if check:
            print('Все записи удалены!')
        else:
            print('Еще не создано ни одной записи!')

    def get_text(self, user_id: int) -> None:
        """Функция вывода на просмотр сохраненного текста"""
        check = self.text_db.get_text_all(user_id)
        if check:
            print(check)
        else:
            print('Запись еще не создана!')
