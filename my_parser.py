from selenium import webdriver
import re

rx_text_img = re.compile(r'<[^<>]+src="([^"<>]+)"[^<>]+>')
rx_text_var = re.compile(r'<i>([^<>]+)</i>')
rx_text = re.compile(r'"([^"]+)"')
rx_nbsp = re.compile(r'&nbsp;')
rx_text_p = re.compile(r'<p>()([ &nbsp;]*)</p>')
rx_right_img = re.compile(r'src="(/get_file\?id=\d+)"')


class Problem:
    number_of_type = int()
    number_of_section = int()
    number_of_problem = int()
    text = str()


class Section:
    def __init__(self):
        self.number_of_type = int()
        self.number_of_section = int()
        self.name_of_section = str()
        self.count_of_problems = int()
        self.source_of_problems = str()
        self.problems = list()


class Category:
    def __init__(self):
        self.number_of_category = int()
        self.name_of_category = str()
        self.count_of_problems = int()
        self.sections = list()


def make_text_nice(x, html_text):
    x_search = x.search(html_text)
    while x_search:
        html_text = re.sub(x, x_search.group(1), html_text, 1)
        x_search = x.search(html_text)
    return html_text


def open_new_window(current_section, source, args):
    with getattr(webdriver, args[0])(f"{args[1]}") as dr:
        dr.get(source)

        for i in range(200):
            dr.implicitly_wait(50)
            dr.find_element_by_tag_name('body').send_keys(
                webdriver.common.keys.Keys.END)

        for i, problem in enumerate(
                dr.find_elements_by_class_name(
                    "problem_container")):
            current_problem = Problem()
            current_problem.number_of_problem = i + 1
            """for text in problem.find_element_by_class_name(
                    'pbody').find_elements_by_class_name('left_margin'):
                html_text = text.get_attribute('innerHTML')
                # html_text = make_text_nice(rx_text_img, html_text)
                # html_text = make_text_nice(rx_text_var, html_text)
                # html_text = make_text_nice(rx_text, html_text)
                rx_nbsp_search = rx_nbsp.search(html_text)
                while rx_nbsp_search:
                    html_text = re.sub(rx_nbsp, ' ', html_text, 1)
                    rx_nbsp_search = rx_nbsp.search(html_text)
                current_problem.text += html_text + ' '"""

            html_text = problem.find_element_by_class_name(
                    'pbody').get_attribute('innerHTML')
            """ html_text = make_text_nice(rx_text_img, html_text)
            html_text = make_text_nice(rx_text_var, html_text)
            html_text = make_text_nice(rx_text_p, html_text)
            html_text = make_text_nice(rx_text, html_text)
            rx_nbsp_search = rx_nbsp.search(html_text)
            while rx_nbsp_search:
                html_text = re.sub(rx_nbsp, ' ', html_text, 1)
                rx_nbsp_search = rx_nbsp.search(html_text)"""
            html_text = make_text_nice(rx_text_p, html_text)
            rx_right_img_search = rx_right_img.search(html_text)
            while rx_right_img_search:
                html_text = re.sub(rx_right_img,
                                   'src="https://math-ege.sdamgia.ru'
                                   + rx_right_img_search.group(1) + '"',
                                   html_text, 1)
                rx_right_img_search = rx_right_img.search(html_text)
            current_problem.text = html_text
            current_problem.number_of_type = current_section.number_of_type
            current_problem.number_of_section = \
                current_section.number_of_section
            current_section.problems.append(current_problem)
        return current_section


def get_items_from_site(args, section: str = 'math', indexes: int = 0):
    url = f'https://{section}-ege.sdamgia.ru/prob_catalog'

    # exec(f'driver = webdriver.{args[0]}("{args[1]}")')
    # driver = webdriver .getattribute(args[0])(args[1])
    driver = getattr(webdriver, args[0])(f"{args[1]}")
    driver.get(url)
    categories = driver.find_element_by_class_name(
        "wrapper").find_element_by_class_name(
        "sgia-main-content").find_elements_by_class_name("cat_category")
    rx_type = re.compile(r'.(\d+). (.+)')
    rx_number = re.compile(r'\w+$')
    index = 1
    sect = []
    for category in categories:
        try:
            if index == indexes or not indexes:
                type_name = rx_type.match(
                    category.find_element_by_class_name('cat_name').text)
                current_category = Category()
                current_category.number_of_category = index
                current_category.name_of_category = type_name.group(2)
                current_category.count_of_problems = re.findall(
                    rx_number, category.text)[0]

                for ind, item in enumerate(
                        category.find_elements_by_class_name('cat_category')):
                    current_section = Section()
                    source = item.find_element_by_class_name(
                        "cat_show").get_attribute("href")
                    count = item.find_element_by_class_name("cat_count").text
                    name = item.find_element_by_class_name("cat_name").text
                    current_section.source_of_problems = source
                    current_section.count_of_problems = count
                    current_section.name_of_section = name
                    current_section.number_of_section = ind + 1
                    current_section.number_of_type = index
                    current_category.sections.append(current_section)
                sect.append(current_category)
            if index == indexes:
                return sect[index - 1]
            index += 1
        except:
            continue

        if index > 19:
            break
    driver.close()
    return sect
