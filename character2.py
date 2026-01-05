#Character2 qui ne bouge pas et reste dans la pièce dans laquelle ils sont affectés

class Character2():
    def __init__(self, name, description, current_room, msgs):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs
        # Index pour parcourir les messages cycliquement
        self._msg_index = 0
        # Pool de messages non encore affichés et liste des messages déjà montrés
        try:
            self._msg_pool = list(msgs) if msgs is not None else []
        except Exception:
            self._msg_pool = []
        self._shown_msgs = []

    def __str__(self):
        return f"{self.name} : {self.description}"
    
    def get_msg(self):
        # Aucun message disponible
        if not self.msgs:
            return ""

        # S'assurer que la pool est initialisée
        if not hasattr(self, '_msg_pool') or self._msg_pool is None:
            try:
                self._msg_pool = list(self.msgs)
            except Exception:
                self._msg_pool = []
        # Reconstituer la pool si on a tout épuisé
        if not self._msg_pool:
            # remonter depuis les messages déjà montrés
            try:
                self._msg_pool = list(self._shown_msgs)
            except Exception:
                self._msg_pool = list(self.msgs)
            self._shown_msgs = []

        try:
            # Popper le premier élément (afin de ne plus l'afficher ensuite)
            msg = self._msg_pool.pop(0)
        except Exception:
            return ""

        # Conserver la trace des messages déjà affichés
        try:
            self._shown_msgs.append(msg)
        except Exception:
            pass

        # Afficher pour le joueur et retourner
        try:
            print(f"{self.name} : {msg}")
        except Exception:
            pass
        return msg