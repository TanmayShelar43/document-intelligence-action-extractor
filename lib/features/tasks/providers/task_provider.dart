import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../models/task_model.dart';

class TaskNotifier extends Notifier<List<TaskModel>> {
  @override
  List<TaskModel> build() {
    return [
      TaskModel(
        id: 'task_1',
        title: 'Review non-compete clause in section 4.2',
        documentName: 'Vendor_Agreement_2026.pdf',
        dueDate: DateTime.now().add(const Duration(days: 2)),
        priority: TaskPriority.high,
      ),
      TaskModel(
        id: 'task_2',
        title: 'Submit Q3 tax exemption documentation',
        documentName: 'Q3_Tax_Notice_Urgent.pdf',
        dueDate: DateTime.now().add(const Duration(days: 5)),
        priority: TaskPriority.high,
      ),
      TaskModel(
        id: 'task_3',
        title: 'Verify equipment return policy terms',
        documentName: 'Equipment_Lease_Contract.docx',
        dueDate: DateTime.now().add(const Duration(days: 12)),
        priority: TaskPriority.medium,
      ),
    ];
  }

  void toggleTask(String taskId) {
    state = [
      for (final task in state)
        if (task.id == taskId) task.copyWith(isCompleted: !task.isCompleted) else task
    ];
  }
}

final taskProvider = NotifierProvider<TaskNotifier, List<TaskModel>>(TaskNotifier.new);