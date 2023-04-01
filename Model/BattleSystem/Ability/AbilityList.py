from Model.BattleSystem.Ability.Ability import Ability
from Model.BattleSystem.Debuff.DebuffList import debuff_list
ability0 = Ability("Slash", "Normal", 1, cost=1) #normal attack
ability1 = Ability("Deep Stab", "Normal", 1, debuff_list[0], cost = 2) #cause vulnerable
ability2 = Ability ("Shove", "Normal", int(0), debuff_list[1], cost = 1) #cause weaken
ability3 = Ability("Slice", "Normal", 0.6, debuff_list[2], cost = 1) #cause bleed
ability4 = Ability("Poison Dart", "Normal", 0.5, debuff_list[3], cost = 1) #causes poison
ability5 = Ability("Open Wound", "Normal", .7, special_message = "If enemy bleeds, deal double damage.", cost = 1)
ability6 = Ability("Hemorrhage", "Normal", 1.2, special_message = "If enemy bleeds, inflict Hemorrhage", cost = 2 )
ability7 = Ability("Tri Attack", "Normal", 1, attack_times=3, special_message = "Attack the enemy 3 times", cost = 2)

ability_list = [ability0,
                ability1,
                ability2,
                ability3,
                ability4,
                ability5,
                ability6,
                ability7]