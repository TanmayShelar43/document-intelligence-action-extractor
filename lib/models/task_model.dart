enum TaskPriority { low, medium, high }

class TaskModel {
  final String id;
  final String title;
  final String documentName;
  final DateTime dueDate;
  final TaskPriority priority;
  final bool isCompleted;

  const TaskModel({
    required this.id,
    required this.title,
    required this.documentName,
    required this.dueDate,
    required this.priority,
    this.isCompleted = false,
  });

  TaskModel copyWith({bool? isCompleted}) {
    return TaskModel(
      id: id,
      title: title,
      documentName: documentName,
      dueDate: dueDate,
      priority: priority,
      isCompleted: isCompleted ?? this.isCompleted,
    );
  }
}