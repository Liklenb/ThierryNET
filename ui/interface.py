import random

import flet as ft
import flet.canvas as cv
from core.routing_table import create_routing_table
from core.depth_first_search import dfs_traversal
from core.graph_creation import create_graph
from core.graph import Graph


def get_element_color(element):
    """Retourne la couleur basée sur le niveau de l'élément."""
    return (
        ft.colors.RED if element.tier.value == 1 else
        ft.colors.GREEN if element.tier.value == 2 else
        ft.colors.BLUE
    )


def is_new_position_valid(new_x, new_y, existing_positions):
    """Vérifie si la nouvelle position est valide en considérant la distance minimale. """
    for pos_x, pos_y in existing_positions:
        if abs(new_x - pos_x) < 60 and abs(new_y - pos_y) < 60:
            return False
    return True


class FletGraphInterface:

    def __init__(self, page):
        self.page = page
        self.page.title = "ThierryNET"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.theme = ft.Theme(color_scheme_seed=ft.colors.PINK, use_material3=True)
        self.page.on_view_pop = self.view_pop
        self.page.window_maximizable = False
        self.page.window_resizable = False
        self.page.window_maximized = True

        load_picker = ft.Ref[ft.FilePicker]()
        self.page.overlay.append(ft.FilePicker(on_result=lambda e: self._load_file(e, load_picker), ref=load_picker))

        self.graph = None
        self.highlighted_vertices = []
        self.highlighted_edges = []
        self.vertex_edges = {}
        self.current_path = (-1, -1)

        self.page.views.append(
            ft.View(
                "/",
                controls=[
                    ft.Row(
                        [
                            ft.Image(
                                src="../assets/logo.png",
                                width=250,
                                height=250
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        size=30,
                                        weight=ft.FontWeight.BOLD,
                                        selectable=True,
                                        spans=[ft.TextSpan(text="Welcome to ThierryNET!")],
                                        text_align=ft.TextAlign.CENTER
                                    ),
                                    ft.FilledButton(
                                        text="Get started with new graph",
                                        on_click=lambda _: self._create_graph()
                                    ),
                                    ft.FilledButton(
                                        text="Load an existing graph",
                                        on_click=lambda _: load_picker.current.pick_files(
                                            dialog_title="Charger le graphe",
                                            file_type=ft.FilePickerFileType.CUSTOM,
                                            allowed_extensions=["thierry"],
                                            allow_multiple=False
                                        )
                                    )

                                ]
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=0.1 * self.page.width
                    )
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

        self.page.go("/")

    def _create_graph(self):
        graph = create_graph()

        while not dfs_traversal(graph):
            graph = create_graph()

        self._create_graph_ui(graph)

    def view_pop(self, _: ft.ViewPopEvent):
        self.page.views.pop()
        self.page.go(self.page.views[-1].route)

    def _load_file(self, event: ft.FilePickerResultEvent, picker: ft.Ref[ft.FilePicker]):
        """Charge un graphe à partir d'un fichier."""
        if event.files is None:
            return

        graph = Graph().load_file(picker.current.result.files[0].path)
        self._create_graph_ui(graph)

    def _create_graph_ui(self, graph):
        self.routing_table = create_routing_table(graph)

        canvas = ft.Ref[cv.Canvas]()
        node = ft.Ref[ft.Stack]()
        save_picker = ft.Ref[ft.FilePicker]()

        if len(self.page.overlay) > 1:
            self.page.overlay.pop()

        self.page.overlay.append(
            ft.FilePicker(on_result=lambda e: graph.save_to_file(e.path + ".thierry"), ref=save_picker))

        self.page.views.append(
            ft.View(
                "graph",
                [
                    ft.AppBar(title=ft.Text("Graph"),
                              toolbar_height=self.page.height * 0.1,
                              actions=[
                                  ft.Container(
                                      padding=ft.padding.only(right=20),
                                      content=ft.FilledButton(
                                          text="Save",
                                          icon=ft.icons.SAVE_ROUNDED,
                                          on_click=lambda _: save_picker.current.save_file(
                                              dialog_title="Sauvegarder le graphe",
                                              file_type=ft.FilePickerFileType.CUSTOM,
                                              allowed_extensions=["thierry"]
                                          ),
                                      ),
                                  )
                              ]),

                    cv.Canvas(
                        content=ft.Stack(
                            width=self.page.width,
                            height=self.page.height * 0.85,
                            ref=node
                        ),
                        width=self.page.width,
                        height=self.page.height * 0.85,
                        ref=canvas
                    )
                ]
            )
        )

        existing_positions = []
        for elt in graph.get_vertices():
            self._add_vertex(elt, existing_positions, node, canvas)

        for elt in graph.get_edges():
            self._add_edge_and_weight(elt.vertex1.identifier, elt.vertex2.identifier, elt.weight, node, canvas)

        self.page.go("graph")

    @staticmethod
    def _get_random_position(existing_positions, node: ft.Ref[ft.Stack]):
        """Génère une position aléatoire valide pour un sommet."""
        while True:
            x = random.randint(0, int(node.current.width) - 70)
            y = random.randint(0, int(node.current.height) - 70)
            if is_new_position_valid(x, y, existing_positions):
                return x, y

    def _add_vertex(self, elt, existing_positions, node: ft.Ref[ft.Stack], canvas: ft.Ref[cv.Canvas]):
        """Ajoute un sommet à l'interface utilisateur."""
        color = get_element_color(elt)
        x, y = self._get_random_position(existing_positions, node)
        node.current.controls.append(self._create_gesture_detector(elt, color, x, y, node, canvas))
        existing_positions.append((x, y))
        self.vertex_edges[elt.identifier] = []

    def _create_gesture_detector(self, elt, color, x, y, node: ft.Ref[ft.Stack], canvas: ft.Ref[cv.Canvas]):
        """Crée un détecteur de geste pour un élément avec une couleur spécifiée."""
        return ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,
            drag_interval=40,
            on_vertical_drag_update=lambda e: self._on_pan_update(e, node, canvas),
            on_tap=lambda e: self._on_tap(e, node, canvas),
            left=x,
            top=y,
            content=ft.Container(
                bgcolor=color,
                width=50,
                height=50,
                border_radius=20,
                content=ft.Text(str(elt.identifier + 1)),
                alignment=ft.Alignment(0, 0)
            )
        )

    def _add_edge_and_weight(self, src, dest, weight, stack: ft.Ref[ft.Stack], canvas: ft.Ref[cv.Canvas]):
        """Ajoute une arête entre les sommets source et destination avec un poids donné."""
        line = cv.Line(
            x1=stack.current.controls[src].left + 25,
            y1=stack.current.controls[src].top + 25,
            x2=stack.current.controls[dest].left + 25,
            y2=stack.current.controls[dest].top + 25,
            paint=ft.Paint(color=ft.colors.WHITE, stroke_width=1),
            data=(src, dest)
        )
        canvas.current.shapes.append(line)

        text = cv.Text(
            x=(stack.current.controls[src].left + stack.current.controls[dest].left) / 2,
            y=(stack.current.controls[src].top + stack.current.controls[dest].top) / 2,
            text=str(weight),
            alignment=ft.Alignment(0, 0),
            data=(src, dest)
        )
        canvas.current.shapes.append(text)

        self.vertex_edges[src].append((line, text))
        self.vertex_edges[dest].append((line, text))

    def _on_pan_update(self, e: ft.DragUpdateEvent, node: ft.Ref[ft.Stack], canvas: ft.Ref[cv.Canvas]):
        """Gère la mise à jour de la position du détecteur de geste pendant le déplacement."""
        self.page.mouse_cursor = ft.MouseCursor.MOVE

        max_left = node.current.width - 70
        max_top = node.current.height - 70

        e.control.top = max(0, min(max_top, e.control.top + e.delta_y))
        e.control.left = max(0, min(max_left, e.control.left + e.delta_x))

        self._update_edges(int(e.control.content.content.value) - 1, e.control.left, e.control.top, node)
        canvas.current.update()

    def _update_edges(self, src, x, y, node: ft.Ref[ft.Stack]):
        """Met à jour les arêtes connectées à un sommet donné."""
        for line, text in self.vertex_edges[src]:
            if line.data[0] == src:
                line.x1 = x + 25
                line.y1 = y + 25
                text.x = (x + node.current.controls[line.data[1]].left) / 2
                text.y = (y + node.current.controls[line.data[1]].top) / 2
            else:
                line.x2 = x + 25
                line.y2 = y + 25
                text.x = (x + node.current.controls[line.data[0]].left) / 2
                text.y = (y + node.current.controls[line.data[0]].top) / 2

    def _on_tap(self, e: ft.TapEvent, node: ft.Ref[ft.Stack], canvas: ft.Ref[cv.Canvas]):
        """Gère l'événement de tap sur un sommet."""
        current_vertex_id = int(e.control.content.content.value) - 1

        if self.current_path[0] == current_vertex_id:
            return

        if self.current_path[0] is None or self.current_path[1] is not None:
            self._reset_ui(canvas)
            self.current_path = (current_vertex_id, None)
            self._highlight_vertex(e.control.content, ft.colors.YELLOW_200)
        else:
            self.current_path = (self.current_path[0], current_vertex_id)
            self._highlight_vertex(e.control.content, ft.colors.ORANGE_200)
            self._highlight_path(node)

        canvas.current.update()

    def _reset_ui(self, canvas: ft.Ref[cv.Canvas]):
        """Réinitialise l'UI en effaçant les sélections et en remettant les arêtes à leur état initial."""
        for vertex in self.highlighted_vertices:
            vertex.border = ft.border.all(0, color=ft.colors.TRANSPARENT)
        self.highlighted_vertices = []

        for edge in canvas.current.shapes:
            edge.paint = ft.Paint(color=ft.colors.WHITE, stroke_width=1)

        self.current_path = (None, None)
        self.highlighted_edges = []

    def _highlight_vertex(self, vertex, color):
        """Met en évidence un sommet sélectionné."""
        vertex.border = ft.border.all(5, color=color)
        self.highlighted_vertices.append(vertex)

    def _highlight_path(self, node: ft.Ref[ft.Stack]):
        """Trouve et met en évidence le chemin entre deux sommets sélectionnés."""
        x = self.current_path[0]
        while x != self.current_path[1]:
            if x not in self.current_path:
                node.current.controls[x].content.border = ft.border.all(5, color=ft.colors.PURPLE_200)
                self.highlighted_vertices.append(node.current.controls[x].content)
            result = (x, None)
            x = self.routing_table[x][self.current_path[1]]
            result = (result[0], x)
            self.highlighted_edges.append(result)

        for x, y in self.highlighted_edges:
            for line, _ in self.vertex_edges[x]:
                if line.data[1] == y or line.data[0] == y:
                    line.paint = ft.Paint(color=ft.colors.RED, stroke_width=10)
                    break
