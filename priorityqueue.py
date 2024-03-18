class QueueItem:
    def __init__(self, item, priority: int):
        self._item = item
        self._priority = priority

    def get_item(self):
        return self._item

    def get_priority(self):
        return self._priority

    def __lt__(self, other):
        if isinstance(other, QueueItem):
            return self._priority < other.get_priority()
        else:
            raise TypeError('Item must be an QueueItem')

    def __eq__(self, other):
        if isinstance(other, QueueItem):
            return self._priority == other.get_priority()
        else:
            raise TypeError('Item must be an QueueItem')


class Queue:
    def __init__(self):
        self._elements: list[QueueItem] = []

    def add(self, item: QueueItem):
        """
        Add an item to the queue
        :param item: The item to add
        :return: None
        """
        if isinstance(item, QueueItem):
            for i in range(len(self._elements)):
                if item.get_priority() < self._elements[i].get_priority():
                    self._elements.insert(i, item)
                    return
            self._elements.append(item)
        else:
            raise TypeError('Item must be an QueueItem')

    def pop(self) -> QueueItem:
        return self._elements.pop(0)

    def __len__(self):
        return len(self._elements)

    def get(self, i: int) -> QueueItem:
        return self._elements[i]
