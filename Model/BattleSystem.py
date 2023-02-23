class BattleSystem():

    def __init__(self, player, entity):
        self.player = player
        self.entity = entity
        self.default_player_ap = 3
        self.player_ap = self.default_player_ap
        self.enemy_attack_idx = 0
        self.enemy_attack_pattern_map = {"attack": entity.attack, "guard": entity.guard}

    def playerAttacks(self):
        if self.player_ap > 0:
            self.player.attack(self.entity)
            self.player_ap -= 1

    def playerTurnEnd(self):
        self.player_ap = self.default_player_ap
        print("\n")#formatting
        self.enemyAttacks()

    def enemyAttacks(self):
        if self.enemy_attack_idx >= len(self.entity.getAttackPattern()) :
            self.enemy_attack_idx = 0
        enemy_next_move = self.enemy_attack_pattern_map[self.entity.getAttack(self.enemy_attack_idx)](self.player)
        enemy_next_move #perform enemy next move
        self.enemy_attack_idx += 1
        print("\n")#formatting

    def getCurrentAP(self):
        return self.player_ap
    def commenceBattle(self):
        player_actions = ("Attack", "Defend", "Escape")
        while self.player.isAlive() and self.entity.isAlive() and self.player_ap > 0:
            print("Enemy HP: " + str(self.entity.getHp()))
            print("Current AP: " + str(self.player_ap))
            player_action = input(player_actions)
            if player_action == player_actions[0]:
                self.playerAttacks()
            elif player_action == player_actions[1]:
                self.player.guard(self.entity)
            elif player_action == player_actions[2]:
                print("You ran away")
                break
            if self.player_ap == 0:
                self.playerTurnEnd()
        print("You win!")


