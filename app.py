from flask import Flask, render_template
import my_parser

app = Flask(__name__)
subjects = {'math': []}
HEAD_FOR_PAGE = '<!DOCTYPE html> \
<html lang="en"> \
<head> \
    <meta charset="UTF-8"> \
    <title>Title</title> \
</head> \
<body> \
<table>'
END_FOR_PAGE = '</table> \
</body> \
</html>'

def make_subjects(name: str):
    if not subjects[name]:
        subjects[name] = my_parser.get_items_from_site(name)


@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route('/<name>-ege')
def get_subject_page(name: str):
    make_subjects(name)
    return render_template('sections.html', categories=subjects[name],
                           name=name)


@app.route('/<name>-ege/<number>')
def get_task_number_page(name: str, number: int):
    make_subjects(name)
    number = int(number)
    if not subjects[name][number - 1].number_of_category:
        subjects[name][number - 1] = my_parser.get_items_from_site(
            name, number)
    section_number_page = HEAD_FOR_PAGE
    for section in subjects[name][number - 1].sections:
        if not section.problems:
            section = my_parser.open_new_window(
                section, section.source_of_problems)
    for section in subjects[name][number - 1].sections:
        for problem in section.problems:
            section_number_page += f'<tr><th>Задание ' \
                               f'{problem.number_of_type}</th></tr> \n\
                               <tr><th>{problem.text}</th></tr>\n'
    section_number_page += END_FOR_PAGE
    return section_number_page
    """return render_template('problem_number.html',
                           category=subjects[name][number - 1])"""


@app.route('/<name>-ege/<number>/<section>')
def get_section_number_page(name: str, number: int, section: int):
    make_subjects(name)
    number = int(number)
    section = int(section)
    if not subjects[name][number - 1].sections[section - 1].problems:
        subjects[name][number - 1].sections[section - 1] = \
            my_parser.open_new_window(
                subjects[name][number - 1].sections[section - 1],
                subjects[name][number - 1].sections[
                    section - 1].source_of_problems)
    section_number_page = HEAD_FOR_PAGE
    for problem in subjects[name][number - 1].sections[section - 1].problems:
        section_number_page += f'<tr><th>Задание ' \
                               f'{problem.number_of_type}</th></tr> \n\
                               <tr><th>{problem.text}</th></tr>\n'
    section_number_page += END_FOR_PAGE
    return section_number_page
    """return render_template('section_number.html', section=subjects[name][
        number - 1].sections[section - 1])"""


if __name__ == '__main__':
    app.run()
