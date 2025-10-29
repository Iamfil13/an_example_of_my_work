import time
from datetime import datetime, timedelta

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.locators import BaseLocators


class Main(BasePage):

    def authorization(self, login, password):
        self.wait_or_report(BaseLocators.LOGIN_PAGE, 'Страница входа не открывается')

        self.wait_until_element_displayed(BaseLocators.LOGIN_USERNAME).send_keys(login)
        self.find_element(BaseLocators.LOGIN_PASSWORD).send_keys(password)
        self.find_element(BaseLocators.SIGN_BUTTON).click()

        self.wait_or_report(BaseLocators.SERVICE_MANAGER_WINDOW, 'Главная страница не открывается')
        self.wait_until_element_not_displayed(BaseLocators.PRELOADER)

    def creating_new_change(self):
        self.wait_until_element_displayed(BaseLocators.CHANGE_MANAGEMENT_BUTTON).click()
        self.wait_until_element_displayed(BaseLocators.CREATE_NEW_CHANGE_BUTTON).click()
        self.wait_or_report(BaseLocators.CHANGE_MODEL_TITTLE, 'Форма с выбором моделей Изменения не открывается')

        self.switch_to_frame(1)
        self.find_element(BaseLocators.SEARCH_FIELD).send_keys('Normal Significant RFC')
        self.find_element(BaseLocators.FIND_BUTTON).click()

        self.wait_or_report(BaseLocators.FOUND_MODEL, 'Модель изменения по названию не найдена')
        self.find_element(BaseLocators.FOUND_MODEL).click()
        time.sleep(1)
        self.find_element(BaseLocators.FOUND_MODEL).click()
        self.wait_or_report(BaseLocators.CREATE_ZNI_FORM, 'Форма создания Обычного ЗНИ не открывается')

    def input_zni_fields(self):
        self.wait_until_element_not_displayed(BaseLocators.PRELOADER)

        self.wait_until_element_displayed(BaseLocators.SERVICE_FIELD).send_keys('Тестовый ЕМИАС(CI9954462)')
        self.wait_until_element_displayed(BaseLocators.SERVICE_SELECT)
        self.find_element(BaseLocators.BODY).send_keys(Keys.ENTER)
        self.wait_until_element_not_displayed(BaseLocators.SERVICE_SELECT)

        self.find_element(BaseLocators.WORKING_GROUP).send_keys('Тестовая РГ')

        self.find_element(BaseLocators.KE_FIELD).send_keys('Тестовая КЕ ЕМИАС')
        self.wait_until_element_displayed(BaseLocators.KE_SELECT)
        self.find_element(BaseLocators.BODY).send_keys(Keys.ENTER)
        self.wait_until_element_not_displayed(BaseLocators.KE_SELECT)

        date = datetime.today() + timedelta(days=7)
        formatted_date = date.strftime("%d/%m/%Y %H:%M:%S")
        self.find_element(BaseLocators.DATE_INPUT).send_keys(formatted_date)

        self.find_element(BaseLocators.SHORT_DESCRIPTION_FIELD).send_keys('Тест')
        self.find_element(BaseLocators.DESCRIPTION_FIELD).click()
        self.find_element(BaseLocators.DESCRIPTION_INPUT_FIELD).send_keys('Тест')

        self.switch_to_default_content()
        self.find_element(BaseLocators.SAVE_BUTTON).click()
        time.sleep(3)
        self.find_element(BaseLocators.SAVE_BUTTON).click()

        self.wait_until_element_not_displayed(BaseLocators.PRELOADER)

    def creating_zni_task(self):
        self.switch_to_frame(1)
        self.find_element(BaseLocators.TASKS_BUTTON).click()
        self.wait_until_element_not_displayed(BaseLocators.PRELOADER)

        self.find_element(BaseLocators.BODY).send_keys(Keys.PAGE_UP)
        self.find_element(BaseLocators.CREATE_TASK_BUTTON).click()

        self.wait_or_report(BaseLocators.REG_TASK_TITTLE, 'Карточка регистрации Задачи не открывается')

        self.wait_until_element_not_displayed(BaseLocators.PRELOADER)
        self.wait_until_element_displayed(BaseLocators.RESPONSIBLE_FIELD).send_keys('АРИСТОВ АРТУР')
        self.wait_until_element_displayed(BaseLocators.RESPONSIBLE_SELECT)

        self.switch_to_default_content()
        self.wait_until_element_displayed(BaseLocators.SAVE_BUTTON).click()
        self.wait_until_element_not_displayed(BaseLocators.PRELOADER)
        self.switch_to_frame(1)
        assert self.find_element(BaseLocators.ZNI_STATUS).get_attribute('value') == 'Запланировано', \
            'В значении ЗНИ Статус не указано "Запланировано"'

        self.switch_to_default_content()
        self.wait_until_element_displayed(BaseLocators.SAVE_AND_EXIT_BUTTON).click()
        self.wait_until_element_not_displayed(BaseLocators.PRELOADER)

        self.switch_to_frame(1)
        self.wait_or_report(BaseLocators.CREATED_TASK, 'Во вкладке Задачи не отображается номер связанной задачи')

        assert self.find_element(BaseLocators.CREATED_TASK_PHASE).text == 'Ожидание', \
            'В значении ЗНИ Фаза не указано "Ожидание"'
        assert self.find_element(BaseLocators.CREATED_TASK_STATUS).text == 'Запланировано', \
            'В значении ЗНИ Статус не указано "Запланировано"'

    def coordination_zni(self):
        self.switch_to_default_content()
        self.find_element(BaseLocators.FOR_PLANNING_BUTTON).click()
        self.wait_until_element_not_displayed(BaseLocators.PRELOADER)

        if self.is_element_present_and_wait(BaseLocators.OK_BUTTON):
            self.find_element(BaseLocators.OK_BUTTON).click()

        self.wait_until_element_not_displayed(BaseLocators.PRELOADER)
        self.switch_to_frame(1)
        assert self.find_element(BaseLocators.ZNI_NEW_STATUS).get_attribute('value') == 'Планирование', \
            'В значении ЗНИ Статус не указано "Планирование"'

        self.switch_to_default_content()
        self.find_element(BaseLocators.SAVE_BUTTON).click()
        self.wait_until_element_not_displayed(BaseLocators.PRELOADER)

        time.sleep(3)
        self.find_element(BaseLocators.REFRESH_BUTTON).click()

        if self.is_element_present_and_wait(BaseLocators.YES_BUTTON):
            self.wait_until_element_displayed(BaseLocators.YES_BUTTON).click()
            self.wait_until_element_displayed(BaseLocators.OK_BUTTON).click()
            self.wait_until_element_not_displayed(BaseLocators.PRELOADER)

        self.find_element(BaseLocators.ON_APPROVAL_BUTTON).click()
        self.wait_until_element_displayed(BaseLocators.OK_BUTTON).click()
        self.wait_until_element_not_displayed(BaseLocators.PRELOADER)

        self.switch_to_frame(1)
        assert self.find_element(BaseLocators.ZNI_NEW_STATUS).get_attribute('value') == 'Согласование', \
            'В значении ЗНИ Статус не указано "Согласование"'

        time.sleep(3)
        for _ in range(8):
            self.find_element(BaseLocators.RIGHT_BUTTON).click()

        self.find_element(BaseLocators.APPROVAL_BUTTON).click()
        self.wait_or_report(BaseLocators.APPROVAL_TAB, 'Нет перехода на вкладку "Согласование"')

        self.find_element(BaseLocators.COORDINATION_TYPE_BUTTON).click()
        self.wait_until_element_displayed(BaseLocators.COORDINATION_TYPE_SELECT).click()

        self.find_element(BaseLocators.COORDINATION_LIST).click()
        self.wait_until_element_displayed(BaseLocators.COORDINATION_LIST_SELECT).click()

        self.find_element(BaseLocators.START_AGREEMENT).click()
        self.switch_to_default_content()
        self.wait_until_element_displayed(BaseLocators.OK_BUTTON).click()
        self.wait_until_element_not_displayed(BaseLocators.PRELOADER)

        self.switch_to_frame(1)
        self.wait_until_element_is_clickable(BaseLocators.APPROVE_BUTTON).click()

    def activation_zni_task(self):
        self.wait_until_element_not_displayed(BaseLocators.MESSAGE)
        self.find_element(BaseLocators.TASKS_BUTTON).click()
        self.wait_or_report(BaseLocators.TASKS_NUMBER, 'Во вкладке "Задачи" не отображается созданная ранее задача')
        number_zni = self.find_element(BaseLocators.TASKS_NUMBER).text

        self.wait_until_element_not_displayed(BaseLocators.MESSAGE)
        self.find_element(BaseLocators.TASKS_NUMBER).click()
        self.wait_or_report((By.XPATH, f"//h2[text()='Задача изменения — {number_zni}']"),
                            f'Карточка задачи № {number_zni} не открывается')

        self.switch_to_default_content()
        self.wait_until_element_not_displayed(BaseLocators.MESSAGE)
        self.wait_until_element_displayed(BaseLocators.ACTIVATE_BUTTON).click()
        self.wait_until_element_not_displayed(BaseLocators.MESSAGE)

        self.switch_to_frame(1)
        assert self.find_element(BaseLocators.ZNI_PHASE).get_attribute('value') == 'Активно', \
            'В значении ЗНИ Фаза не указано "Активно"'

        # TODO Отсутствует кнопка "В работу"
        # self.switch_to_default_content()
        # self.wait_until_element_displayed(BaseLocators.TO_WORK_BUTTON).click()

    def execution_zni_task(self):
        self.find_element(BaseLocators.COMMENT_CLOSE_CLICK).click()
        self.find_element(BaseLocators.COMMENT_CLOSE_FIELD).send_keys('Тест')
        self.find_element(BaseLocators.CODE_CLOSE_FIELD).send_keys('1')
        self.find_element(BaseLocators.BODY).send_keys(Keys.ENTER)

        # TODO Отсутствует кнопка "Выполнить"
        self.switch_to_default_content()
        self.wait_until_element_displayed(BaseLocators.SAVE_AND_EXIT_BUTTON).click()
        self.wait_until_element_not_displayed(BaseLocators.PRELOADER)

        # Поиск нужного ЗНИ
        # self.wait_until_element_displayed(BaseLocators.SEARCH_ZNI_BUTTON).click()
        # self.wait_until_element_not_displayed(BaseLocators.PRELOADER)
        # self.switch_to_frame(2)
        # self.wait_until_element_displayed(BaseLocators.SEARCH_ZNI_FIELD).send_keys(number_zni)
        # self.switch_to_default_content()
        # self.wait_until_element_displayed(BaseLocators.SEARCH_BUTTON).click()
        # self.wait_until_element_not_displayed(BaseLocators.PRELOADER)
