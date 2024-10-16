import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

refeicao = ctrl.Antecedent(np.arange(0, 11, 1), 'refeicao')
servico = ctrl.Antecedent(np.arange(0, 11, 1), 'servico')
tempo_atendimento = ctrl.Antecedent(np.arange(0, 11, 1), 'tempo_atendimento')
gorjeta = ctrl.Consequent(np.arange(0, 26, 1), 'gorjeta')

refeicao['insossa'] = fuzz.trimf(refeicao.universe, [0, 0, 5])
refeicao['mediana'] = fuzz.trimf(refeicao.universe, [0, 5, 10])
refeicao['saborosa'] = fuzz.trimf(refeicao.universe, [5, 10, 10])

servico['ruim'] = fuzz.trimf(servico.universe, [0, 0, 5])
servico['medio'] = fuzz.trimf(servico.universe, [0, 5, 10])
servico['excelente'] = fuzz.trimf(servico.universe, [5, 10, 10])

tempo_atendimento['demorado'] = fuzz.trimf(tempo_atendimento.universe, [0, 0, 5])
tempo_atendimento['mediano'] = fuzz.trimf(tempo_atendimento.universe, [0, 5, 10])
tempo_atendimento['rapido'] = fuzz.trimf(tempo_atendimento.universe, [5, 10, 10])

gorjeta['pouca'] = fuzz.trimf(gorjeta.universe, [0, 0, 13])
gorjeta['media'] = fuzz.trimf(gorjeta.universe, [0, 13, 25])
gorjeta['generosa'] = fuzz.trimf(gorjeta.universe, [13, 25, 25])
gorjeta['sem_gorjeta'] = fuzz.trimf(gorjeta.universe, [0, 0, 0])


rule1 = ctrl.Rule(refeicao['insossa'] & servico['ruim'] & tempo_atendimento['rapido'] | tempo_atendimento['mediano'], gorjeta['pouca'])
rule2 = ctrl.Rule(refeicao['saborosa'] & servico['excelente'] & (tempo_atendimento['rapido'] | tempo_atendimento['mediano']), gorjeta['generosa'])
rule3 = ctrl.Rule(tempo_atendimento['demorado'], gorjeta['sem_gorjeta'])  

sistema_gorjeta = ctrl.ControlSystem([rule1, rule2, rule3])
sistema_simulador = ctrl.ControlSystemSimulation(sistema_gorjeta)

try:
    refeicao_input = float(input("Avalie a refeição de 0 (insossa) a 10 (saborosa): "))
    servico_input = float(input("Avalie o serviço de 0 (ruim) a 10 (excelente): "))
    tempo_atendimento_input = float(input("Avalie o tempo de atendimento de 0 (demorado) a 10 (rápido): "))

    if 0 <= refeicao_input <= 10 and 0 <= servico_input <= 10 and 0 <= tempo_atendimento_input <= 10:
        sistema_simulador.input['refeicao'] = refeicao_input
        sistema_simulador.input['servico'] = servico_input
        sistema_simulador.input['tempo_atendimento'] = tempo_atendimento_input

        sistema_simulador.compute()

        print(f"Percentual de gorjeta sugerido: {sistema_simulador.output['gorjeta']:.2f}%")
    else:
        print("Por favor, insira valores entre 0 e 10 para todas as avaliações.")
except ValueError:
    print("Entrada inválida. Por favor, insira números válidos.")
