from Model.BattleSystem.Ability.Ability import Ability
from Model.BattleSystem.Debuff.DebuffList import debuff_list
ability0 = Ability("Slash", "Normal", 1, cost=1) #normal attack
ability1 = Ability("Deep Stab", "Normal", 1, debuff_list[0], cost = 2) #cause vulnerable
ability2 = Ability ("Shove", "Normal", int(0), debuff_list[1], cost = 1) #cause weaken
ability3 = Ability("Gashing Strike", "Normal", 1.1, debuff_list[2]) #cause bleed
ability4 = Ability("Poison Dart", "Normal", 0.5, debuff_list[3]) #causes poison

ability_list = [ability0,
                ability1,
                ability2,
                ability3,
                ability4]