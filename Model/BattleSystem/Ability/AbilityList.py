from Model.BattleSystem.Ability.Ability import Ability
import Model.BattleSystem.Debuff.DebuffList as d
ability0 = Ability("Deep Stab", "Normal", 1.2, d.debuff_list[0]) #cause vulnerable
ability1 = Ability ("Tail Whip", "Normal", int(0), d.debuff_list[1]) #cause weaken
ability2 = Ability("Gashing Strike", "Normal", 1.1, d.debuff_list[2]) #cause bleed

ability_list = [ability0,
                ability1,
                ability2]