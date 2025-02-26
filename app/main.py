import hashlib
import toml
from typing import Any
from pathlib import Path

def get_md5_hash(input_string: str) -> str:
    """
    Вычисляет MD5 хеш для заданной строки.
    """

    # Кодируем строку в байты, если она представлена в виде Unicode.
    encoded_string = input_string.encode('utf-8')
    # Создаем объект MD5.
    md5_hash = hashlib.md5()
    # Обновляем объект хеша данными.
    md5_hash.update(encoded_string)
    # Получаем хеш в шестнадцатеричном формате.
    hex_digest = md5_hash.hexdigest()
    return hex_digest

def get_config() -> dict[str, Any]:
    """
    Загружает данные конфигурации программы.
    """
    current_dir: Path = Path.cwd()
    parent_dir: Path = current_dir.parent
    config_file: Path = parent_dir / "config.toml"
    with open(config_file, "r") as f:
        config = toml.load(f)
    return config
  

if __name__ == "__main__":
    hash_input_password: str = get_md5_hash("12345")
    config: dict[str, Any] = get_config()

    if(config["user"]["password"] != hash_input_password):
        print("Неверный пароль.")
    else:
        print("Добро пожаловать.")


     



  




