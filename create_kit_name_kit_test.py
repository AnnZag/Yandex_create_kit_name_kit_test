import sender_stand_request
import data

def get_kit_body(name):
    current_body = data.kit_body.copy()
    current_body["name"] = name
    return current_body

def get_new_user_token():
    # Создать нового клиента
    user_body = data.user_body
    resp_user = sender_stand_request.post_new_user(user_body)
    # Запомнить токен авторизации
    return resp_user.json()["authToken"]

# Проверка успешного создания набора с данным именем:
def positive_assert(kit_body):
    # Создать новый набор
    resp_kit = sender_stand_request.post_new_client_kit(kit_body, get_new_user_token())
    # Проверить код ответа
    assert resp_kit.status_code == 201
    # Проверить, что имя в ответе совпадает с именем в запросе
    assert resp_kit.json()["name"] == kit_body["name"]

# Проверка получения ошибки при невалидном теле запроса (код 400)
def negative_assert_code_400(kit_body):
    resp = sender_stand_request.post_new_client_kit(kit_body, get_new_user_token())
    assert resp.status_code == 400

# Тест 1. Успешное создание набора. (Параметр name состоит из 1ого символа)
def test_create_kit_1_letter_in_kit_name_get_success_response():
    kit_body = get_kit_body("a")
    positive_assert(kit_body)

# Тест 2. Успешное создание набора. (Параметр name состоит из 511 символов)
def test_create_kit_511_letters_in_name_get_success_response():
    kit_body = get_kit_body("Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
                            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
                            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
                            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
                            "abcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
                            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
                            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
                            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
                            "abcdabcdabcdabcdabcdabcdabcdabC")
    positive_assert(kit_body)

# Тест 3. Ошибка
# Параметр kit_name состоит из пустой строки
def test_create_kit_empty_kit_name_get_error_response():
    kit_body = get_kit_body("")
    negative_assert_code_400(kit_body)

# Тест 4. Ошибка
# Параметр kit_name состоит из 512 символов
def test_create_kit_512_letter_in_kit_name_get_error_response():
    kit_body = get_kit_body("Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
                            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
                            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
                            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
                            "abcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
                            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
                            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
                            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
                            "abcdabcdabcdabcdabcdabcdabcdabaC")
    negative_assert_code_400(kit_body)

# Тест 5. Успешное создание набора
# Параметр kit_name состоит из английских букв
def test_create_kit_english_letters_in_kit_name_get_success_response():
    kit_body = get_kit_body("QWErty")
    positive_assert(kit_body)

# Тест 6. Успешное создание набора
# Параметр kit_name состоит из русских букв
def test_create_kit_russian_letters_in_kit_name_get_success_response():
    kit_body = get_kit_body("Мария")
    positive_assert(kit_body)

# Тест 7. Успешное создание набора
# Параметр kit_name состоит из строки спецсимволов
def test_create_kit_has_special_simbol_in_kit_name_get_success_response():
    kit_body = get_kit_body("/№%@,")
    positive_assert(kit_body)

# Тест 8. Успешное создание набора
# Параметр kit_name состоит из слов с пробелами
def test_create_kit_has_space_in_kit_name_get_success_response():
    kit_body = get_kit_body(" Человек и КО ")
    positive_assert(kit_body)

# Тест 9. Успешное создание набора
# Параметр kit_name состоит из строки с цифрами
def test_create_kit_has_number_in_kit_name_get_success_response():
    kit_body = get_kit_body("123")
    positive_assert(kit_body)

# Тест 10. Ошибка
# В запросе нет параметра kit_name
def test_create_kit_no_kit_body_get_error_response():
    # Копируется словарь с телом запроса из файла data в переменную kit_body
    # Чтобы не потерять данные из исходного словаря
    kit_body = data.kit_body.copy()
    # Удаление параметра kit_body из запроса
    kit_body.pop("name")
    # Проверка полученного ответа
    negative_assert_code_400(kit_body)

# Тест 11. Ошибка
# Передан другой тип данных в параметре kit_name
def test_create_kit_has_wrong_data_type_in_kit_name_get_error_response():
    kit_body = get_kit_body(123)
    negative_assert_code_400(kit_body)
