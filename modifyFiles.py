import os 
import shutil
import audiosegment
import numpy as np
import matplotlib.pyplot as plt
import gc

def modifyFiles(target_folder, original_folder_dir, sample_rate):
    for subfolder in os.listdir(original_folder_dir):  
        try:
            shutil.rmtree(os.path.join(target_folder, subfolder))
            print("dir " + str(os.path.join(target_folder, subfolder)) + " deleted, overwriting")
        except Exception as e:
            print(e)
        new_sub_dir = os.path.join(target_folder, subfolder)
        try:
            os.mkdir(new_sub_dir)
            print("↑created new dir")
        except Exception as e:
            print(e)

        for file in os.listdir(os.path.join(original_folder_dir, subfolder)):
            print(file)
            print(os.path.abspath(file))
            if os.path.isdir(os.path.join(original_folder_dir, subfolder, file)) == False:
                new_file_name = file.split("-")[2] + "-" + file.split("-")[3] + "-" + file.split("-")[4] + "-" + file.split("-")[5] + "-" + file.split("-")[6]
                os.mkdir(os.path.join(new_sub_dir, new_file_name))
                shutil.copyfile(os.path.join(original_folder_dir, subfolder, file), os.path.join(new_sub_dir, new_file_name, new_file_name))
                change_sample_rate(sample_rate, os.path.join(new_sub_dir, new_file_name, new_file_name))
                spectrogram(os.path.join(new_sub_dir, new_file_name, new_file_name), os.path.join(new_sub_dir, new_file_name))
                gc.collect()
                    
            else:
                try:
                    os.mkdir(os.path.join(new_sub_dir, file))
                    print("↑created new file")
                except Exception as e:
                    print(e)
                for sub_file in os.listdir(os.path.join(original_folder_dir, subfolder, file)):
                    new_file_name = sub_file.split("-")[2] + "-" + sub_file.split("-")[3] + "-" + sub_file.split("-")[4] + "-" + sub_file.split("-")[5] + "-" + sub_file.split("-")[6]
                    os.mkdir(new_sub_dir, file, sub_file)
                    shutil.copyfile(os.path.join(original_folder_dir, subfolder, file, sub_file), os.path.join(new_sub_dir, file, sub_file, sub_file))  
                    change_sample_rate(sample_rate, os.path.join(new_sub_dir, file, sub_file, sub_file))
                    spectrogram(os.path.join(new_sub_dir, file, sub_file, sub_file), os.path.join(new_sub_dir, file, sub_file))
                    gc.collect()

def change_sample_rate(sample_rate, audio_file_path):
    sound = audiosegment.from_file(audio_file_path)
    new_sound = sound.set_frame_rate(sample_rate)
    new_sound.export(audio_file_path, format="wav")

def fft(file, output_dir):
    audio = audiosegment.from_file(file)
    samples = np.array(audio.get_array_of_samples())
    fft_output = np.fft.fft(samples)
    fft_magnitude = np.abs(fft_output)
    plt.figure(figsize=(12, 6))
    plt.plot(fft_magnitude)
    plt.title("fft_" + file.split("/")[-1].split(".")[0])
    plt.xlabel("Frequency")
    plt.ylabel("Magnitude")
    plt.savefig(os.path.join(output_dir, "fft_" + file.split("/")[-1].split(".")[0]))
    plt.clf()
    plt.close()

def spectrogram(file, output_dir):
    seg = audiosegment.from_file(file)
    freqs, times, amplitudes = seg.spectrogram(window_length_s=0.03, overlap=0.5)
    amplitudes = 10 * np.log10(amplitudes + 1e-9)
    print(freqs.dtype)
    print(times.dtype)
    print(amplitudes.dtype)
    Y,X=np.meshgrid(freqs, times)
    plt.figure(figsize=(10, 4))
    plt.pcolormesh(Y, X, amplitudes.astype(float), shading='auto')
    plt.title("spectrogram " + file.split("/")[-1].split(".")[0])
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.savefig(os.path.join(output_dir, "spectrogram_" + file.split("/")[-1].split(".")[0]))
    plt.clf()
    plt.close()


def main():
    modifyFiles(r"/home/filip/Documents/praxe2024/archive_processed", r"/home/filip/Documents/praxe2024/archive", 19000)

main()
