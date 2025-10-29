import allure

from conftest import step_wrapper
from pages.main_page import Main
from pages.metrics import config


@allure.feature('MFSM')
@allure.suite('MFSM. Стандартный ЗНИ. Работа с основным флоу')
@allure.story('MFSM. Стандартный ЗНИ. Работа с основным флоу')
def test_mfsm_appeals(browser, metrics, api_client):
    """
        Наименование сценария:
        Стандартный ЗНИ. Работа с основным флоу
        https://wiki.mos.social/pages/viewpage.action?pageId=952639822

        Шаг 1. Авторизация
            Открыть в браузере страницу
            http://10.2.162.14:8080/smnoldap/index.do
            Ввести
            логин: ###
            пароль: ###
            Нажать "Войти"

        Шаг 2. Создание нового изменения
            Нажать "Управление изменениями" в меню слева
            Нажать "Создание нового изменения"
            Ввести в поиск Normal Significant RFC  и нажать Enter
            Нажать на Normal Significant RFC

        Шаг 3. Заполнение полей ЗНИ
            Заполнить поля карточки :
                Тип изменения = Управление изменениями ТЕСТ
                Сервис = Тестовый ЕМИАС(CI9954462)
                Рабочая группа = Тестовая РГ
                КЕ = Тестовая КЕ ЕМИАС
                Плановое начало = сегодня + 7 дней
                Краткое описание: тест
            Нажать "Сохранить"

        Шаг 4. Создание задачи ЗНИ
            Нажать на вкладку "Задачи"
            Нажать кнопку Создать задачу
            Заполнить поле "Ответственный" - АРИСТОВ АРТУР
            Нажать кнопку "Сохранить"
            Нажать кнопку "Сохранить и выйти"

        Шаг 5. Согласование ЗНИ
            Нажать "На планирование"
            Нажать "На согласование"
            Нажать "Согласование" (для этого стрелкой промотать вправо)
            Заполнить поля
                Тип согласования = Все
                Список согласующих = АРИСТОВ АРТУР
            Нажать кнопку Запустить согласование
            Нажать кнопку Согласовать

        Шаг 6. Активация задачи ЗНИ
            Нажать на вкладку "Задачи"
            Нажать на номер задачи
            Нажать кнопку "Активировать"
            Нажать кнопку "В работу"

        Шаг 7. Выполнение задачи ЗНИ
            Комментарии по закрытию = тест
            Код закрытия = 1 - Успешно (выбор из выпадающего списка)
            Нажать кнопку "Выполнить"
            Нажать кнопку "Сохранить и выйти"
            Нажать кнопку "Обновить"
            Нажать кнопку "Закрыть"

        """

    metrics.set_job("mfsm_regular_zni_main_flow")
    metrics.set_job_desc("MFSM. Обычный ЗНИ. Работа с основным флоу")

    api_client.set_job("mfsm_regular_zni_main_flow")
    api_client.set_job_desc("MFSM. Обычный ЗНИ. Работа с основным флоу")

    login = config['login']
    password = config['password']
    link = config['url']
    critical_time = 60

    step_name = '01_authorization'
    step_desc = 'Шаг 01: Авторизация'
    with step_wrapper(step_name, step_desc, critical_time, browser, metrics, api_client):
        page = Main(browser, link)
        page.open()
        page.authorization(login, password)

    step_name = '02_creating_new_change'
    step_desc = 'Шаг 02: Создание нового изменения'
    with step_wrapper(step_name, step_desc, critical_time, browser, metrics, api_client):
        page.creating_new_change()

    step_name = '03_input_zni_fields'
    step_desc = 'Шаг 03: Заполнение полей ЗНИ'
    with step_wrapper(step_name, step_desc, critical_time, browser, metrics, api_client):
        page.input_zni_fields()

    step_name = '04_creating_zni_task'
    step_desc = 'Шаг 04: Создание задачи ЗНИ'
    with step_wrapper(step_name, step_desc, critical_time, browser, metrics, api_client):
        page.creating_zni_task()

    step_name = '05_coordination_zni'
    step_desc = 'Шаг 05: Согласование ЗНИ'
    with step_wrapper(step_name, step_desc, critical_time, browser, metrics, api_client):
        page.coordination_zni()

    step_name = '06_activation_zni_task'
    step_desc = 'Шаг 06: Активация задачи ЗНИ'
    with step_wrapper(step_name, step_desc, critical_time, browser, metrics, api_client):
        page.activation_zni_task()

    step_name = '07_execution_zni_task'
    step_desc = 'Шаг 07: Выполнение задачи ЗНИ'
    with step_wrapper(step_name, step_desc, critical_time, browser, metrics, api_client):
        page.execution_zni_task()
