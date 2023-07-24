import datetime
import json
from dataclasses import dataclass, is_dataclass, asdict, field

@dataclass
class Specialization:
    timestamp: datetime.datetime = 0
    faculty: str = ''
    spec_name: str = ''
    plan_all: int = 0
    plan_goal: int = 0
    plan_paid: int = 0
    got_all: int = 0
    got_goal: int = 0
    got_no_exams: int = 0
    got_no_comp: int = 0
    got_with_comp: int = 0
    amounts: list[int] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.timestamp, str):
            #'2023-07-23T16:03:00'
            self.timestamp = datetime.datetime.strptime(self.timestamp, '%Y-%m-%dT%H:%M:%S')

    def __getitem__(self, key):
        return self.amounts[key]

    def __eq__(self, other):
        if not isinstance(other, Specialization):
            return False

        for a, b in zip(self.__dict__, other.__dict__):
            if a != b:
                return False
        return True

    def __str__(self):
        return f'''План приема:
    факультет: {self.faculty}
    специальность: {self.spec_name}
    всего: {self.plan_all}
    целевое: {self.plan_goal}
    оплата: {self.plan_paid}

Подано:
    всего: {self.got_all}
    целевое: {self.got_goal}
    без вступительных экзаменов: {self.got_no_exams}
    вне конкурса: {self.got_no_comp}
    по конкурсу: {self.got_with_comp}

Баллы:
    ''' + '\n\t'.join([f'{i} - {i - 4}: {amount}' for i, amount in zip(range(400, 119, -5), self.amounts)])


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        return super().default(o)