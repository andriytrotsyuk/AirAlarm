import 'package:flutter/material.dart';

class InstructionDialog extends StatelessWidget {
  const InstructionDialog({super.key});

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Інструкція'),
      content: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            _buildSectionTitle(context, 'Перед запуском'),
            _buildListItem(
                '1. Підключіть до комп\'ютера гучномовець чи інший пристрій для програвання аудіо'),
            _buildListItem(
                '2. Забезпечте комп\'ютер доступом до мережі Інтернет.'),
            const SizedBox(height: 16),
            _buildSectionTitle(context, 'Як користуватись'),
            _buildListItem(
                '1. Почніть вводити назву регіону в пошуку та оберіть потрібний.'),
            _buildListItem(
                '2. Налаштуйте тривалість програвання тривоги (за потреби).'),
            _buildListItem(
                '3. Статус регіону відобразиться на екрані. Якщо все добре — сирена лунатиме при тривозі.'),
            const SizedBox(height: 16),
            _buildSectionTitle(context, 'Функції'),
            _buildListItem(
                '• При тривозі сирена лунає 3 хвилини (можна змінити).'),
            _buildListItem('• При відбої тривоги лунає голосове сповіщення.'),
            const SizedBox(height: 8),
            Text(
              'Додатково:',
              style: Theme.of(context).textTheme.titleSmall,
            ),
            _buildListItem('• О 9:00 — хвилина мовчання.'),
            _buildListItem('• О 9:01 — гімн України.'),
            _buildListItem('• Автозапуск при старті системи.'),
          ],
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('Зрозуміло'),
        ),
      ],
    );
  }

  Widget _buildSectionTitle(BuildContext context, String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8.0),
      child: Text(
        title,
        style: Theme.of(context).textTheme.titleMedium?.copyWith(
              fontWeight: FontWeight.bold,
            ),
      ),
    );
  }

  Widget _buildListItem(String text) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 4.0),
      child: Text(
        text,
        style: const TextStyle(height: 1.4),
      ),
    );
  }
}
