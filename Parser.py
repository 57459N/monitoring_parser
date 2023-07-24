import re
import datetime
import requests

from Specialization import Specialization


class Parser:
    url = 'https://abit.bsu.by/formk1?id=32'

    time_mask = r'<span id="Abit_K11_lbCurrentDateTime">(.*?)</span>'
    faculty_mask = r'<td class="fl" colspan="68"><font color="Black">.*?</font></td>[\s\S]*?<td colspan="68"><font color="Black">&nbsp;</font></td>'
    faculty_name_mask = r'<td class="fl" colspan="68"><font color="Black">(.*?)</font></td>'
    specs_mask = r'<td class="vl"><font color="Black">.*'
    spec_name_mask = r'<td class="vl"><font color="Black">(.*?)</font></td><td>'
    spec_values_mask = r'">(\d*?)<'

    faculties_names_mask = r'<td class="fl" colspan="68"><font color="Black">(.*?)<'
    specs_by_faculty_mask = r'<td class="fl" colspan="68"><font color="Black">(.*{}.*[\S\s]*?)<td colspan="68"><font color="Black">&nbsp;</font></td>'

    def __init__(self):
        self.parsed_time = 0
        self.content = ''
        self.update()

    def get_parsed_time(self, content: str) -> datetime.datetime:
        return datetime.datetime.strptime(re.findall(self.time_mask, content)[0], '%d.%m.%Y %H:%M')

    def update(self) -> bool:
        new_content = requests.get(self.url).text
        parse_time = self.get_parsed_time(new_content)

        if parse_time != self.parsed_time:
            self.content = new_content
            self.parsed_time = parse_time
            return True
        return False


    def get_all(self, save_html=False):
        parse_time = self.get_parsed_time(self.content)

        if save_html:
            with open(f'html/{parse_time.strftime("%d.%m.%Y_%H.%M")}.html', 'w', encoding='windows-1251') as f:
                f.write(self.content)

        faculties_texts = re.findall(self.faculty_mask, self.content)

        result = {}
        for faculty_text in faculties_texts:
            faculty_name = re.findall(self.faculty_name_mask, faculty_text)[0].strip()
            result[faculty_name] = self.get_specs_from_falulty_text(faculty_text, parse_time, faculty_name)

            # with open(file_path, 'w', encoding='utf-8') as f:
            #     json.dump(Specialization(parse_time, faculty_name, spec_name, *values[1:9], values[9:]),
            #               f,
            #               cls=EnhancedJSONEncoder,
            #               default=str)
            #     print(Specialization(*json.load(f).values()))
            #     json.dump(specs[0], f, cls=EnhancedJSONEncoder)

        return result

    # def get_specs

    def get_specs_from_falulty_text(self, specs_text: str, parse_time: datetime.datetime, faculty_name: str) \
            -> dict[str, Specialization]:
        result = {}
        specs = re.findall(self.specs_mask, specs_text)
        for spec in specs:
            spec_name = re.findall(self.spec_name_mask, spec)[0].strip()
            values = re.findall(self.spec_values_mask, spec)
            values = [int(i) if i else 0 for i in values]

            result[spec_name] = Specialization(parse_time,
                                               faculty_name,
                                               spec_name,
                                               *values[1:9],
                                               values[9:])
        return result

    def get_faculties_names(self) -> list[str]:
        return [i.strip() for i in re.findall(self.faculties_names_mask, self.content)]

    def get_specs_by_faculty(self, faculty: str) -> dict[str, Specialization]:
        pattern = self.specs_by_faculty_mask.format(faculty)
        text = re.findall(pattern, self.content)[0]
        full_faculty_name = text[:text.index('<')]
        return self.get_specs_from_falulty_text(text, self.parsed_time, full_faculty_name)