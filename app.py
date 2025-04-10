from flask import Flask, render_template, request

app = Flask(__name__)

class Edge:
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight

class Subset:
    def __init__(self, parent, rank):
        self.parent = parent
        self.rank = rank

def find(subsets, i):
    if subsets[i].parent != i:
        subsets[i].parent = find(subsets, subsets[i].parent)
    return subsets[i].parent

def union(subsets, x, y):
    xroot = find(subsets, x)
    yroot = find(subsets, y)

    if subsets[xroot].rank < subsets[yroot].rank:
        subsets[xroot].parent = yroot
    elif subsets[xroot].rank > subsets[yroot].rank:
        subsets[yroot].parent = xroot
    else:
        subsets[yroot].parent = xroot
        subsets[xroot].rank += 1

def kruskalMST(edges, numNodes):
    edges.sort(key=lambda e: e.weight)
    subsets = [Subset(i, 0) for i in range(numNodes)]
    result = []
    e = i = 0

    while e < numNodes - 1 and i < len(edges):
        next_edge = edges[i]
        i += 1
        x = find(subsets, next_edge.src)
        y = find(subsets, next_edge.dest)

        if x != y:
            result.append(next_edge)
            union(subsets, x, y)
            e += 1
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    result_html = ''
    if request.method == 'POST':
        try:
            numNodes = int(request.form['numNodes'])
            edgesText = request.form['edgesText'].strip()
            lines = edgesText.splitlines()

            edges = []
            for i, line in enumerate(lines):
                parts = line.strip().split()
                if len(parts) != 3:
                    result_html = f"<span style='color:red;'>❌ Invalid format at line {i+1}. Expected: src dest weight</span>"
                    break
                src, dest, weight = map(int, parts)
                if src < 0 or dest < 0 or src >= numNodes or dest >= numNodes:
                    result_html = f"<span style='color:red;'>❌ Invalid node index at line {i+1}</span>"
                    break
                edges.append(Edge(src, dest, weight))

            if len(edges) < numNodes - 1:
                result_html = f"<span style='color:red;'>❗ At least {numNodes - 1} edges required to form MST.</span>"
            else:
                mst = kruskalMST(edges, numNodes)
                total_length = sum(e.weight for e in mst)
                output = ""
                for e in mst:
                    output += f"Computer {e.src} -- Computer {e.dest} ➝ Cable Length {e.weight}<br>"
                output += f"<br><strong>Total Cable Length Needed:</strong> {total_length}"
                result_html = output

        except Exception as e:
            result_html = f"<span style='color:red;'>Error: {str(e)}</span>"

    return render_template("index.html", result=result_html)

if __name__ == '__main__':
    app.run(debug=True)
