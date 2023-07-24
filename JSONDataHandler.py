from Specialization import Specialization, EnhancedJSONEncoder
import json
import pathlib
from typing import Callable


class JSONDataHandler:
    @staticmethod
    def get_file_name(spec: Specialization):
        return spec.timestamp.strftime('%d.%m.%Y_%H.%M')

    def save_all(self, _path: str, data: dict[str, dict[str, Specialization]]) -> None:
        def save_spec(_path: pathlib.Path, spec: Specialization):
            if not _path.exists():
                _path.mkdir(parents=True)

            _path = _path.joinpath(self.get_file_name(spec) + '.json')
            with _path.open('w', encoding='utf-8') as f:
                json.dump(spec,
                          f,
                          cls=EnhancedJSONEncoder)

        for fac_name, specs in data.items():
            for spec_name, spec in specs.items():
                path = pathlib.Path(_path).joinpath(fac_name, spec_name)
                save_spec(path, spec)

    @staticmethod
    def read_last(data_dir_path: str) -> dict[str, dict[str, Specialization]]:
        def max_created_time(o: pathlib.Path):
            return o.stat().st_ctime

        def read_file(p: pathlib.Path) -> Specialization:
            with p.open('r', encoding='utf-8') as f:
                return Specialization(*json.load(f).values())

        result = {}

        path = pathlib.Path(data_dir_path)
        for fac_dir in path.iterdir():
            result[fac_dir.stem] = {}
            if not fac_dir.is_dir():
                continue
            for spec_dir in fac_dir.iterdir():
                if not spec_dir.is_dir():
                    continue
                json_files = [i for i in spec_dir.iterdir() if i.suffix == '.json']
                result[fac_dir.stem][spec_dir.stem] = read_file(max(json_files, key=max_created_time))

        return result

    def read_all_of_spec(self, path_of_spec_dir: str):
        pass
