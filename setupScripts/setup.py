from commands import commands
from commandIO import saveCommands
from makalaughIO import saveMakaLaugh
from specialCheckRuleIO import saveSpecialCheckRules

saveCommands(commands)
saveMakaLaugh()
saveSpecialCheckRules()
input("Success. Press any key to exit.")