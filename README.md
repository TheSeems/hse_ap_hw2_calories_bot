# Calories Bot

Сделано в рамках домашнего задания по дисциплине "Прикладной Python"

Бот (работоспособность не гарантирована): [@my_calories_for_hw2_ap_bot](https://t.me/my_calories_for_hw2_ap_bot)

## Команды

- `/start`
    - Начать работу с ботом
- `/set_profile`
    - Настроить профиль:
        - Вес, рос, возраст
        - Уровень активности
        - Город (Open Weather Map)
        - Цель калорий
- `/log_water`
- `/log_workout`
- `/log_food` (Open Food Facts)

## Screencast

[Screencast.mov](Screencast.mov)

[Screencast.mp4](Screencast.mp4)

## Локальный запуск

- Сконфигурировать [.env](.env) файл - указать токен бота и OpenWeatherMap (`test_mode` лучше оставить `false`)
- ```commandline
  docker build . -t hse_ap_hw2_calories_bot:latest
  docker run hse_ap_hw2_calories_bot
  ```

