import time
import logging
import sqlite3
import platform
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Функция для чтения учетных данных из файла
def read_accounts_from_file(file_path):
    accounts = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                data = line.strip().split(";")
                if len(data) == 4:
                    email, password, new_password, username = data
                    accounts.append((email, password, new_password, username))
        logging.info("Учетные данные успешно прочитаны из файла.")
    except Exception as e:
        logging.error(f"Ошибка при чтении учетных данных из файла: {e}")
    return accounts


# Функция для обработки учетной записи на Galxe и Twitter
def automate_galxe_and_twitter(email, password, new_password, twitter_username):
    try:
        driver = webdriver.Chrome()
        try:
            # Переход на сайт Galxe
            driver.get("https://app.galxe.com/quest/MindNetwork/GC9C8tTgaP")
            time.sleep(3)

            # Нажатие на кнопку "Login"
            login_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[4]/div[2]/div/div[1]/div/div/div[2]/div/div/div/button/div[1]/div[2]/div',
                    )
                )
            )
            login_button.click()
            time.sleep(4)

            menu = driver.find_element(By.CLASS_NAME, "login-item-wrapper")
            actions = ActionChains(driver)
            actions.move_to_element(menu)
            actions.click(menu)
            actions.perform()
            time.sleep(5)

            actions = ActionChains(driver)
            actions.send_keys(Keys.ESCAPE)
            actions.perform()
            time.sleep(5)

            driver.current_window_handle
            wait = WebDriverWait(driver, 10)
            original_window = driver.current_window_handle
            assert len(driver.window_handles) == 2


            wait.until(EC.number_of_windows_to_be(2))

            # Проходим цикл, пока не найдем новый дескриптор окна.
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break

            driver.switch_to.window(window_handle)

            # Вводим email и пароль для входа
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            time.sleep(2)
            email_input.send_keys(email)
            email_input.send_keys(Keys.ENTER)
            time.sleep(2)

            # Проверка необходимости ввода имени пользователя после почты
            try:
                username_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "text"))
                )
                if username_input:
                    username_input.send_keys(twitter_username)
                    username_input.send_keys(Keys.ENTER)
                    time.sleep(3)
            except TimeoutException:
                print("Имя пользователя после email не требуется")

            password_input = driver.find_element(By.NAME, "password")
            password_input.send_keys(password)
            password_input.send_keys(Keys.ENTER)
            time.sleep(3)

            click = driver.find_element(
                By.XPATH,
                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/div/div/div[1]/div[3]/div',
            )
            actions = ActionChains(driver)
            actions.move_to_element(click)
            actions.click(click)
            actions.perform()
            time.sleep(10)

            driver.switch_to.window(original_window)
            time.sleep(4)

            time.sleep(4)
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(4)

            actions = ActionChains(driver)
            actions.send_keys(Keys.ESCAPE)
            actions.perform()
            logging.info("Кнопка ESC нажата")
            time.sleep(3)
            driver.refresh()
            time.sleep(3)

            logging.info("ОКНО БЫЛО ЗАКРЫТО")

            # Шаг 1: Найдите и нажмите на кнопку репоста (ретвита) на странице Galxe
            repost_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[2]/div[2]/div/img',
                    )
                )  
            )
            repost_button.click()
            logging.info("Нажата кнопка репоста.")

            # Шаг 2: Переключитесь на новое окно
            original_window = (
                driver.current_window_handle
            )  # Сохраняем дескриптор исходного окна
            WebDriverWait(driver, 15).until(
                EC.number_of_windows_to_be(2)
            )  # Ждем, пока появится второе окно
            new_window = [
                window for window in driver.window_handles if window != original_window
            ][
                0
            ]  
            driver.switch_to.window(new_window)  # Переключитесь на новое окно
            logging.info("Переключился на новое окно для публикации поста.")

            # Шаг 3: Найдите и нажмите на кнопку для публикации поста
            publish_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/div/div/div/div/div[3]/div/div[2]/div/span/span',
                    )
                )  
            )

            publish_button.click()
            logging.info("Нажата кнопка для публикации поста.")
            time.sleep(5)

            # Шаг 4: Вернитесь обратно к исходному окну
            driver.switch_to.window(original_window)
            logging.info("Вернулся к исходному окну.")
            time.sleep(5)

            subscribe_button = driver.find_element(
                By.XPATH,
                '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[1]/div[1]/div/div[1]/div',
            )
            subscribe_button.click()

            logging.info("Нажата кнопка подписки.")
            time.sleep(5)  # Пауза для завершения действий на странице

            # Сохранение результатов в базу данных
            save_to_database(email, twitter_username)
            logging.info(f"Обработка учетной записи {email} завершена.")

        except Exception as e:
            logging.error(f"Ошибка при обработке учетной записи {email}: {e}")

    finally:
        # Закрытие веб-драйвера
        driver.quit()


# Функция для сохранения данных в базу данных SQLite
def save_to_database(email, twitter_username):
    try:
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS account_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                twitter_username TEXT NOT NULL
            )
        """
        )

        cursor.execute(
            """
            INSERT INTO account_info (email, twitter_username)
            VALUES (?, ?)
        """,
            (email, twitter_username),
        )

        conn.commit()
        logging.info("Данные учетной записи успешно сохранены в базу данных.")

    except Exception as e:
        logging.error(f"Ошибка при сохранении данных в базу данных: {e}")

    finally:
        # Закрытие соединения с базой данных
        conn.close()


# Основная функция для чтения учетных данных и их обработки
def main():
    file_path = "account.txt"

    accounts = read_accounts_from_file(file_path)
    for account in accounts:
        email, password, new_password, twitter_username = account
        logging.info(f"Обработка учетной записи: {email}")
        automate_galxe_and_twitter(email, password, new_password, twitter_username)


if __name__ == "__main__":
    main()
