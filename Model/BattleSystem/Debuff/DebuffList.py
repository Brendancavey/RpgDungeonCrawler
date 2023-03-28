from Model.BattleSystem.Debuff.Debuff import Debuff
debuff0 = Debuff("Vulnerable", 2, 1, 2, "Receive 50% additional incoming direct-damage.")
debuff1 = Debuff("Weakened", 2, 2, .25, "Outdoing direct damage is reduced by 25%.")
debuff2 = Debuff("Bleed", 2, 0, 2, "Receive 2 damage to hp per turn.")
debuff3 = Debuff("Poison", 10, 0, 1, "Receive 1 damage to hp per turn.")
debuff_list = [debuff0,
               debuff1,
               debuff2,
               debuff3]