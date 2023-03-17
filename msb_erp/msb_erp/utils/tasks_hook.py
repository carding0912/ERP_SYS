from celery import Task


class HookTask(Task):
    """
    任务钩子:监控任务的执行情况
    """
    def on_success(self, retval, task_id, args, kwargs):  # 正常执行
        print('retval',retval)
        print('task_id',task_id)

    def on_failure(self, exc, task_id, args, kwargs, e_info):   # 执行失败
        print(f'task_id:{task_id},arg:{args},failed ! error_info:{e_info}')

    def on_retry(self, exc, task_id, args, kwargs, e_info):   # 重试执行
        print(f'task id{task_id},args:{args}, retry ! error_info:{e_info}')