from Model.BattleSystem.Ability.Ability import Ability
from Model.BattleSystem.Debuff.DebuffList import debuff_list
ability0 = Ability("Deep Stab", "Normal", 1.2, debuff_list[0]) #cause vulnerable
ability1 = Ability ("Tail Whip", "Normal", int(0), debuff_list[1]) #cause weaken
ability2 = Ability("Gashing Strike", "Normal", 1.1, debuff_list[2]) #cause bleed
ability3 = Ability("Poison Dart", "Normal", 0.5, debuff_list[3]) #causes poison

ability_list = [ability0,
                ability1,
                ability2,
                ability3]