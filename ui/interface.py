import flet as ft
import flet.canvas as cv
import random


def _get_color(elt):
    """Retourne la couleur basée sur le niveau de l'élément."""
    return (
        ft.colors.RED if elt.tier.value == 1 else
        ft.colors.GREEN if elt.tier.value == 2 else
        ft.colors.BLUE
    )


def _is_position_valid(x, y, existing_positions):
    """Vérifie si la nouvelle position est valide en considérant la distance minimale. """
    for pos_x, pos_y in existing_positions:
        if abs(x - pos_x) < 60 and abs(y - pos_y) < 60:
            return False
    return True


class FletInterface:
    def __init__(self, page, graph, table_routage):
        """Initialise l'interface utilisateur Flet avec une page et un graphe donnés."""
        self.page = page
        self.graph = graph
        self.table_routage = table_routage
        self.existing_positions = []
        self.current_path = (None, None)
        self.colored_vertices = []
        self.colored_edges = []
        self._configure_page()
        self._create_minimal_ui()
        self.page.update()
        self.graph_saved = []

    def _configure_page(self):
        """Configure les propriétés de la page."""
        self.page.title = "ThierryNET"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.theme = ft.Theme(color_scheme_seed=ft.colors.PINK, use_material3=True)
        self.page.on_resize = self._page_resize

    def _create_minimal_ui(self):
        """Crée une interface utilisateur lorsque la fenêtre n'est pas maximisée."""
        self.page.controls = [ft.Row([
            ft.Text("L'application ne fonctionne que si la fenêtre est maximisée.")],
            alignment=ft.MainAxisAlignment.CENTER)
        ]

    def _create_maximal_ui(self):
        """Crée l'interface utilisateur principale avec les sommets et les arêtes quand la fenêtre est maximisée."""

        self.stack = ft.Stack(width=self.page.width,
                              height=self.page.height)

        self.cv = cv.Canvas(content=self.stack,
                            width=self.page.width + self.page.window_left,
                            height=self.page.height + self.page.window_top)

        for elt in self.graph.get_vertices():
            self._add_vertex(elt)

        del self.existing_positions

        for elt in self.graph.get_edges():
            self._add_edge_and_weight(elt.vertex1.identifier, elt.vertex2.identifier, elt.weight)

        del self.graph

        self.page.controls = [self.cv]

    def _get_random_position(self):
        """Génère une position aléatoire valide pour un sommet."""
        while True:
            x = random.randint(0, int(self.stack.width) - 70)
            y = random.randint(0, int(self.stack.height) - 70)
            if _is_position_valid(x, y, self.existing_positions):
                return x, y

    def _create_gesture_detector(self, elt, color, x, y):
        """Crée un détecteur de geste pour un élément avec une couleur spécifiée."""
        return ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,
            drag_interval=30,
            on_vertical_drag_update=self._on_pan_update,
            on_tap=self._on_tap,
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

    def _page_resize(self, e):
        """Gère l'événement de redimensionnement de la page."""
        if not e.control.window_maximized:
            self._create_minimal_ui()
            if not self.graph_saved:
                self.graph_saved = self.cv
        else:
            if self.graph_saved:
                self.page.controls = [self.graph_saved]
            else:
                self._create_maximal_ui()

        self.page.update()

    def _on_pan_update(self, e: ft.DragUpdateEvent):
        """Gère la mise à jour de la position du détecteur de geste pendant le déplacement."""
        self.page.mouse_cursor = ft.MouseCursor.MOVE

        max_left = self.stack.width - 70
        max_top = self.stack.height - 70

        e.control.top = max(0, min(max_top, e.control.top + e.delta_y))
        e.control.left = max(0, min(max_left, e.control.left + e.delta_x))

        self._update_edges(int(e.control.content.content.value), e.control.left, e.control.top)
        self.cv.update()

    def _add_vertex(self, elt):
        """Ajoute un sommet à l'interface utilisateur."""
        color = _get_color(elt)
        x, y = self._get_random_position()
        self.stack.controls.append(self._create_gesture_detector(elt, color, x, y))
        self.existing_positions.append((x, y))

    def _update_edges(self, src, x, y):
        """Met à jour les arêtes connectées à un sommet donné."""
        for edge in self.cv.shapes:
            if type(edge) is cv.Text:
                if edge.data[0] == src:
                    edge.x = (x + self.stack.controls[edge.data[1]-1].left) / 2
                    edge.y = (y + self.stack.controls[edge.data[1]-1].top) / 2
                elif edge.data[1] == src:
                    edge.x = (x + self.stack.controls[edge.data[0]-1].left) / 2
                    edge.y = (y + self.stack.controls[edge.data[0]-1].top) / 2
            else:
                if edge.data[0] == src:
                    edge.x1 = x + 25
                    edge.y1 = y + 25
                elif edge.data[1] == src:
                    edge.x2 = x + 25
                    edge.y2 = y + 25

    def _add_edge_and_weight(self, src, dest, weight):
        """Ajoute une arête entre les sommets source et destination avec un poids donné."""
        self.cv.shapes.append(cv.Line(
            x1=self.stack.controls[src].left + 25,
            y1=self.stack.controls[src].top + 25,
            x2=self.stack.controls[dest].left + 25,
            y2=self.stack.controls[dest].top + 25,
            paint=ft.Paint(color=ft.colors.WHITE, stroke_width=1),
            data=(src + 1, dest + 1)
        ))

        self.cv.shapes.append(cv.Text(
            x=(self.stack.controls[src].left + self.stack.controls[dest].left) / 2,
            y=(self.stack.controls[src].top + self.stack.controls[dest].top) / 2,
            text=str(weight),
            alignment=ft.Alignment(0, 0),
            data=(src + 1, dest + 1)
        ))

    def _on_tap(self, e: ft.TapEvent):
        """Gère l'événement de tap sur un sommet."""
        current_vertex_id = int(e.control.content.content.value) - 1

        if len(self.colored_vertices) >= 2:
            self._reset_ui()

        if self.current_path[0] is None:
            self.current_path = (current_vertex_id, None)
            self._highlight_vertex(e.control.content, ft.colors.BLUE_200)
        elif self.current_path[1] is None:
            self.current_path = (self.current_path[0], current_vertex_id)
            self._highlight_vertex(e.control.content, ft.colors.PINK_200)
            self._highlight_path()

        self.cv.update()

    def _reset_ui(self):
        """Réinitialise l'UI en effaçant les sélections et en remettant les arêtes à leur état initial."""
        for vertex in self.colored_vertices:
            vertex.border = ft.border.all(0, color=ft.colors.TRANSPARENT)
        self.colored_vertices = []

        for edge in self.cv.shapes:
            edge.paint = ft.Paint(color=ft.colors.WHITE, stroke_width=1)

        self.current_path = (None, None)
        self.colored_edges = []

    def _highlight_vertex(self, vertex, color):
        """Met en évidence un sommet sélectionné."""
        vertex.border = ft.border.all(5, color=color)
        self.colored_vertices.append(vertex)

    def _highlight_path(self):
        """Trouve et met en évidence le chemin entre deux sommets sélectionnés."""
        x = self.current_path[0]
        while x != self.current_path[1]:
            if x not in self.current_path:
                self.stack.controls[x].content.border = ft.border.all(5, color=ft.colors.PURPLE_200)
                self.colored_vertices.append(self.stack.controls[x].content)
            result = (x, None)
            x = self.table_routage[x][self.current_path[1]]
            result = (result[0], x)
            self.colored_edges.append(result)

        for x, y in self.colored_edges:
            for edge in self.cv.shapes:
                if ((edge.data[0] == x + 1 and edge.data[1] == y + 1) or
                        (edge.data[0] == y + 1 and edge.data[1] == x + 1)):
                    edge.paint = ft.Paint(color=ft.colors.RED, stroke_width=10)
                    break
