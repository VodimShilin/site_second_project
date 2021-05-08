'<!DOCTYPE html> \
<html lang="en"> \
<head> \
    <meta charset="UTF-8"> \
    <title>Title</title> \
</head> \
<body> \
    <table> \
        {% for problem in section.problems %} \
        <tr> \
            <th> \
                Задание {{ problem.number_of_type }} \
            </th> \
        </tr> \
        <tr> \
            <th>problem.text</th> \
        </tr> \
        {% endfor %} \
    </table> \
</body> \
</html> '
