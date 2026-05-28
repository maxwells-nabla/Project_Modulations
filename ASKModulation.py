import numpy as np
import scipy
import plotly.graph_objects as go

# First, let me define a signal with random zeros and ones

numBits = 100000 # Number of bits 
fs = 100000  # sampling rate (samples/second)
fc = 5000  # carrier frequency (Hz)
ns = 100 # Samples per bit
duration = (numBits*ns) / fs  # seconds

list_snr = []
list_ber = []
list_theo_ber = []

for i in range(0, 21, 1):

    snr = i

    array_bits = np.random.randint(0, 2, numBits)

    # Now, I have to simulate a sine function to do AM modulation

    signal = np.repeat(array_bits, ns)

    t = np.arange(0, duration, 1 / fs)  # time array
    carrier = np.sin(2 * np.pi * fc * t)

    ask_signal = np.multiply(signal, carrier)

    # Show figure

    # fig = go.Figure()

    # fig.add_trace(go.Scatter(x = t, y = ask_signal, mode="lines", name="ASK signal"))

    # fig.show()

    # Normalisation of the signal before adding AGWN

    power_in = np.mean(np.square(ask_signal))


    normalised_ask = (1/np.sqrt(power_in))*ask_signal

    # fig = go.Figure()
    
    # fig.add_trace(go.Scatter(x = t, y = normalised_ask, mode="lines", name="ASK signal"))
    
    # fig.show() 

    # I compute the linear snr

    snr_linear = 10**(snr/10)

    # Generate random noise (additive gaussian white noise)

    noise = np.random.normal(0, np.sqrt(1/snr_linear), size=len(normalised_ask))

    noisy_ask = noise + normalised_ask

    # fig = go.Figure()

    # fig.add_trace(go.Scatter(x = t, y = noisy_ask, mode="lines", name="ASK signal"))

    # fig.show()

    # I obtain the envelope of the signal via the Hilbert transform

    envelope = np.abs(scipy.signal.hilbert(noisy_ask))

    normalised_envelope = (envelope - min(envelope)) / (max(envelope) - min(envelope))

    # I reorganise my array into the shape needed for doing the mean of the repeated values

    reshaped_envelope = np.reshape(normalised_envelope, (numBits, ns))

    # I get the recovered signal

    signal_reconstructed_mean = np.mean(reshaped_envelope, axis=1)

    # I apply the threshold ( > 0.5)

    array_bits_reconstructed = (signal_reconstructed_mean > 0.5).astype(int)

    # I compare both signals

    errors = np.sum(array_bits_reconstructed != array_bits)

    # I get the BER

    ber = errors / numBits

    # I get the theoretical BER

    theo_ber = 0.5 * scipy.special.erfc(np.sqrt(snr_linear / 2))

    # Append the results to the lists

    list_snr.append(snr)

    list_ber.append(ber)

    list_theo_ber.append(theo_ber)



# Convert the lists to arrays

array_snr = np.array(list_snr)
array_ber = np.array(list_ber)
array_theo_ber = np.array(list_theo_ber)

# Graph the result

fig = go.Figure()

fig.add_trace(go.Scatter(x=array_snr, y=array_ber, mode="lines+markers", name="Empirical BER"))
fig.add_trace(go.Scatter(x=array_snr, y=array_theo_ber, mode="lines", name="Theoretical BER"))

fig.update_layout(
    yaxis_type="log",
    xaxis_title="SNR (dB)",
    yaxis_title="BER",
    title="BER vs SNR — ASK Modulation"
)

fig.show()
















