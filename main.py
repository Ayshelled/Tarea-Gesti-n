import numpy as np
import matplotlib.pyplot as plt
from funciones import (
    data, promedio_movil, naive, acumulado, exponencial,
    weighted_moving_average, regresion, continueregression,
    calc_md, calc_mad, calc_mse, calc_rmse, calc_mpe, calc_mape, 
    calc_ts, grafico
)

def print_menu():
    """Display the main menu"""
    print("\n" + "="*70)
    print("           SISTEMA DE PRONÓSTICOS DE DEMANDA")
    print("="*70)
    print("a) Promedio Móvil Simple (n=3)")
    print("b) Método Naive")
    print("c) Método Cumulativo/Acumulado")
    print("d) Suavización Exponencial (Alpha=0.4)")
    print("e) Suavización Exponencial (Alpha=0.6)")
    print("f) Suavización Exponencial (Alpha=0.5)")
    print("g) Promedio Móvil Ponderado (w1=0.4, w2=0.6)")
    print("h) Regresión Lineal")
    print("i) Calcular Errores de Todos los Métodos")
    print("j) Señal de Rastreo (Tracking Signal)")
    print("k) Gráfico de Pronósticos")
    print("l) Análisis Comparativo de Todos los Métodos")
    print("s) Salir")
    print("="*70)

def get_forecast_result(method_name, forecast_data):
    """Display forecast results in a formatted table"""
    print(f"\n{'Mes':<12} {'Demanda':<15} {'Pronóstico':<15}")
    print("-" * 42)
    for key, val in forecast_data.items():
        try:
            demand = val['demanda']
            forecast = val['forecast']
            print(f"{key:<12} {demand:<15} {forecast:<15}")
        except (KeyError, TypeError):
            pass

def print_errors(method_name, forecast_data):
    """Display all error metrics"""
    md = calc_md(forecast_data)
    mad = calc_mad(forecast_data)
    mse = calc_mse(forecast_data)
    rmse = calc_rmse(forecast_data)
    mpe = calc_mpe(forecast_data)
    mape = calc_mape(forecast_data)
    
    print(f"\n--- Errores para {method_name} ---")
    print(f"MD (Mean Deviation):        {md:.4f}")
    print(f"MAD (Mean Absolute Dev):    {mad:.4f}")
    print(f"MSE (Mean Squared Error):   {mse:.4f}")
    print(f"RMSE (Root MSE):            {rmse:.4f}")
    print(f"MPE (Mean Percentage Error):{mpe:.4f}")
    print(f"MAPE (Mean Abs % Error):    {mape:.4f}")

def option_a():
    """Simple moving average with n=3"""
    print("\n[a] PROMEDIO MÓVIL SIMPLE (n=3)")
    forecast_data = promedio_movil(3, data)
    get_forecast_result("Promedio Móvil (n=3)", forecast_data)
    print_errors("Promedio Móvil (n=3)", forecast_data)

def option_b():
    """Naive method"""
    print("\n[b] MÉTODO NAIVE")
    forecast_data = naive(data)
    get_forecast_result("Método Naive", forecast_data)
    print_errors("Método Naive", forecast_data)

def option_c():
    """Cumulative/accumulated method"""
    print("\n[c] MÉTODO CUMULATIVO/ACUMULADO")
    forecast_data = acumulado(data)
    get_forecast_result("Método Acumulado", forecast_data)
    print_errors("Método Acumulado", forecast_data)

def option_d():
    """Exponential smoothing with alpha=0.4"""
    print("\n[d] SUAVIZACIÓN EXPONENCIAL (Alpha=0.4)")
    print("(Usando como pronóstico inicial el método Naive para Dic-2024)")
    # Get naive forecast for initialization (last value of 12/24)
    initial_forecast = data["12/24"]
    forecast_data = exponencial(initial_forecast, 0.4, data)
    get_forecast_result("Suavización Exponencial (0.4)", forecast_data)
    print_errors("Suavización Exponencial (0.4)", forecast_data)

def option_e():
    """Exponential smoothing with alpha=0.6"""
    print("\n[e] SUAVIZACIÓN EXPONENCIAL (Alpha=0.6)")
    print("(Usando como pronóstico inicial el método Naive para Dic-2024)")
    initial_forecast = data["12/24"]
    forecast_data = exponencial(initial_forecast, 0.6, data)
    get_forecast_result("Suavización Exponencial (0.6)", forecast_data)
    print_errors("Suavización Exponencial (0.6)", forecast_data)

def option_f():
    """Exponential smoothing with alpha=0.5"""
    print("\n[f] SUAVIZACIÓN EXPONENCIAL (Alpha=0.5)")
    print("(Usando como pronóstico inicial el método Acumulado para Dic-2024)")
    initial_forecast = data["12/24"]  # Using accumulated method
    forecast_data = exponencial(initial_forecast, 0.5, data)
    get_forecast_result("Suavización Exponencial (0.5)", forecast_data)
    print_errors("Suavización Exponencial (0.5)", forecast_data)

def option_g():
    """Weighted moving average"""
    print("\n[g] PROMEDIO MÓVIL PONDERADO (w1=0.4, w2=0.6)")
    print("(w1 corresponde al período más reciente)")
    forecast_data = weighted_moving_average([0.6, 0.4], data)
    get_forecast_result("Promedio Móvil Ponderado", forecast_data)
    print_errors("Promedio Móvil Ponderado", forecast_data)

def option_h():
    """Linear regression"""
    print("\n[h] REGRESIÓN LINEAL")
    m, c = regresion(data)
    print(f"Ecuación: y = {m:.4f}x + {c:.4f}")
    
    # Get original data
    print(f"\n{'Mes':<12} {'Demanda':<15} {'Pronóstico':<15}")
    print("-" * 42)
    x_vals = list(range(1, len(data) + 1))
    for i, (key, value) in enumerate(data.items()):
        forecast = x_vals[i] * m + c
        print(f"{key:<12} {value:<15} {forecast:<15.2f}")
    
    # Forecast for 2025 months
    print("\n--- Pronóstico para meses faltantes de 2025 ---")
    future_months = ["10/25", "11/25", "12/25"]
    future_forecast = continueregression(m, c, 3, data)
    for i, month in enumerate(future_months):
        print(f"{month}: {future_forecast[i]:.2f}")

def option_i():
    """Calculate errors for all methods"""
    print("\n[i] CÁLCULO DE ERRORES PARA TODOS LOS MÉTODOS")
    
    methods = [
        ("Promedio Móvil (n=3)", promedio_movil(3, data)),
        ("Método Naive", naive(data)),
        ("Método Acumulado", acumulado(data)),
        ("Suavización Exponencial (0.4)", exponencial(data["12/24"], 0.4, data)),
        ("Suavización Exponencial (0.6)", exponencial(data["12/24"], 0.6, data)),
        ("Suavización Exponencial (0.5)", exponencial(data["12/24"], 0.5, data)),
        ("Promedio Móvil Ponderado", weighted_moving_average([0.6, 0.4], data)),
    ]
    
    print(f"\n{'Método':<35} {'MD':<12} {'MAD':<12} {'MSE':<12} {'RMSE':<12} {'MPE':<12} {'MAPE':<12}")
    print("-" * 120)
    
    for method_name, forecast_data in methods:
        md = calc_md(forecast_data)
        mad = calc_mad(forecast_data)
        mse = calc_mse(forecast_data)
        rmse = calc_rmse(forecast_data)
        mpe = calc_mpe(forecast_data)
        mape = calc_mape(forecast_data)
        
        print(f"{method_name:<35} {md:<12.4f} {mad:<12.4f} {mse:<12.4f} {rmse:<12.4f} {mpe:<12.4f} {mape:<12.4f}")

def option_j():
    """Tracking signal for exponential smoothing"""
    print("\n[j] SEÑAL DE RASTREO (TRACKING SIGNAL)")
    
    alphas = [0.3, 0.5, 0.7]
    
    for alpha in alphas:
        forecast_data = exponencial(data["12/24"], alpha, data)
        ts = calc_ts(forecast_data)
        print(f"\nAlpha={alpha}: TS = {ts:.4f}")
        
        if -4 <= ts <= 4:
            print(f"  → El proceso está bajo control")
        else:
            print(f"  → El proceso está fuera de control")

def option_k():
    """Display forecast graph"""
    print("\n[k] GRÁFICO DE PRONÓSTICOS")
    print("Seleccione el método:")
    print("1. Promedio Móvil Simple")
    print("2. Método Naive")
    print("3. Método Acumulado")
    print("4. Suavización Exponencial (0.4)")
    print("5. Suavización Exponencial (0.6)")
    print("6. Promedio Móvil Ponderado")
    
    choice = input("Ingrese su opción (1-6): ").strip()
    
    methods = {
        "1": ("Promedio Móvil Simple", promedio_movil(3, data)),
        "2": ("Método Naive", naive(data)),
        "3": ("Método Acumulado", acumulado(data)),
        "4": ("Suavización Exponencial (0.4)", exponencial(data["12/24"], 0.4, data)),
        "5": ("Suavización Exponencial (0.6)", exponencial(data["12/24"], 0.6, data)),
        "6": ("Promedio Móvil Ponderado", weighted_moving_average([0.6, 0.4], data)),
    }
    
    if choice in methods:
        method_name, forecast_data = methods[choice]
        grafico(forecast_data)
    else:
        print("Opción no válida")

def option_l():
    """Comparative analysis of all methods"""
    print("\n[l] ANÁLISIS COMPARATIVO DE TODOS LOS MÉTODOS")
    
    methods = [
        ("Promedio Móvil (n=3)", promedio_movil(3, data)),
        ("Método Naive", naive(data)),
        ("Método Acumulado", acumulado(data)),
        ("Suavización Exponencial (0.4)", exponencial(data["12/24"], 0.4, data)),
        ("Suavización Exponencial (0.6)", exponencial(data["12/24"], 0.6, data)),
        ("Suavización Exponencial (0.5)", exponencial(data["12/24"], 0.5, data)),
        ("Promedio Móvil Ponderado", weighted_moving_average([0.6, 0.4], data)),
    ]
    
    # Calculate best method based on MAPE
    print("\nCálculo de MAPE por método:")
    print("-" * 50)
    
    best_method = None
    best_mape = float('inf')
    mapes = {}
    
    for method_name, forecast_data in methods:
        mape = calc_mape(forecast_data)
        mapes[method_name] = mape
        print(f"{method_name:<35} MAPE: {mape:.4f}")
        
        if mape < best_mape:
            best_mape = mape
            best_method = method_name
    
    print("\n" + "="*50)
    print(f"MEJOR MÉTODO: {best_method}")
    print(f"MAPE más bajo: {best_mape:.4f}")
    print("="*50)
    
    # Create comparison graph
    print("\nGenerando gráfico comparativo...")
    plt.figure(figsize=(14, 8))
    
    x = range(1, len(data) + 1)
    demanda = list(data.values())
    plt.plot(x, demanda, label='Demanda Real', color='black', linestyle='-', linewidth=2, marker='o')
    
    colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink']
    for (method_name, forecast_data), color in zip(methods, colors):
        forecasts = []
        x_positions = []
        for idx, key in enumerate(data.keys()):
            try:
                forecasts.append(forecast_data[key]['forecast'])
                x_positions.append(idx + 1)
            except (KeyError, TypeError):
                pass
        
        if len(forecasts) > 0:
            plt.plot(x_positions, forecasts, label=method_name, linestyle='--', color=color, alpha=0.7)
    
    plt.xlabel('Períodos (Meses)')
    plt.ylabel('Demanda')
    plt.title('Comparación de Métodos de Pronóstico')
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def main():
    """Main function with menu"""
    while True:
        print_menu()
        option = input("Ingrese su opción (a-l o s para salir): ").strip().lower()
        
        try:
            if option == 'a':
                option_a()
            elif option == 'b':
                option_b()
            elif option == 'c':
                option_c()
            elif option == 'd':
                option_d()
            elif option == 'e':
                option_e()
            elif option == 'f':
                option_f()
            elif option == 'g':
                option_g()
            elif option == 'h':
                option_h()
            elif option == 'i':
                option_i()
            elif option == 'j':
                option_j()
            elif option == 'k':
                option_k()
            elif option == 'l':
                option_l()
            elif option == 's':
                print("\n¡Hasta luego!")
                break
            else:
                print("Opción no válida. Por favor, ingrese a-l o s.")
            
            input("\nPresione Enter para continuar...")
        
        except Exception as e:
            print(f"Error: {e}")
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()
