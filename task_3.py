from flask import Flask, jsonify, request, make_response


def appearance(intervals):
    start_lesson, end_lesson = intervals['lesson']
    pupil = intervals['pupil']
    tutor = intervals['tutor']

    first = max(start_lesson, pupil[0], tutor[0])
    last = min(end_lesson, pupil[-1], tutor[-1])

    total = pupil + tutor
    total = sorted([[total[i-1], total[i]] for i in range(1, len(total), 2)],
                   key=lambda x: x[1])
    lines = [(first, total[0][1])]
    right = 0

    for l, r in total:
        if r > last:
            r = last
        if l < right:
            lines.append((l, right))
        elif l < lines[-1][1] and r > lines[-1][1]:
            right = r
        elif l > lines[-1][1]:
            lines.append([l, r])

    count = 0

    for line in lines:
        count += line[1] - line[0]
    return count

print(appearance({
  'lesson': [1594663200, 1594666800],
  'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
  'tutor': [1594663290, 1594663430, 1594663443, 1594666473]
}))

tasks = {
  'lesson': [1594663200, 1594666800],
  'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
  'tutor': [1594663290, 1594663430, 1594663443, 1594666473]
}

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, Tetrika school!"


@app.route('/appearance/<string:key>', methods=['GET'])
def get_appearance(key):
    if key in tasks:
        return jsonify({key: tasks[key]})
    else:
        return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/appearance/total_time', methods=['GET'])
def get_total_time_appearance():
    return jsonify({'appearance': appearance(tasks)})


@app.route('/appearance/add', methods=['POST'])
def add_time():
    if not request.json:
        abort(400)

    for key in request.json.keys():
        if not key in tasks:
            abort(400)

    for key in request.json.keys():
        tasks[key].append(list(map(int, request.json[key].split(" "))))

    return jsonify({'appearance': tasks}), 201


if __name__ == '__main__':
    app.run(debug=True)
