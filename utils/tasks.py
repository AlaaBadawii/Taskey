import json


def build_task_summary(tasks):
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.status == 'completed')
    pending_tasks = total_tasks - completed_tasks
    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
    }


def parse_task_steps(raw_steps):
    cleaned_steps = []
    for step in raw_steps:
        normalized_step = step.strip()
        if normalized_step:
            cleaned_steps.append(normalized_step)
    return cleaned_steps


def build_task_steps(step_texts, completed_states=None):
    completed_states = completed_states or []
    steps = []

    for index, step_text in enumerate(step_texts):
        normalized_step = step_text.strip()
        if not normalized_step:
            continue

        is_completed = False
        if index < len(completed_states):
            is_completed = completed_states[index] == 'true'

        steps.append({
            'text': normalized_step,
            'completed': is_completed,
        })

    return steps


def serialize_task_steps(steps):
    return json.dumps(steps) if steps else None


def deserialize_task_steps(raw_steps):
    if not raw_steps:
        return []

    try:
        parsed_steps = json.loads(raw_steps)
    except (TypeError, ValueError):
        parsed_steps = [raw_steps]

    if not isinstance(parsed_steps, list):
        return []

    normalized_steps = []
    for step in parsed_steps:
        if isinstance(step, str) and step.strip():
            normalized_steps.append({
                'text': step.strip(),
                'completed': False,
            })
        elif isinstance(step, dict):
            text = step.get('text', '').strip()
            if text:
                normalized_steps.append({
                    'text': text,
                    'completed': bool(step.get('completed', False)),
                })

    return normalized_steps
