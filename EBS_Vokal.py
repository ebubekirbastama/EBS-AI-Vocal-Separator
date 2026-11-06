# -*- coding: utf-8 -*-
"""EBS AI Vocal Studio - modern Windows arayuzu.
Demucs modelini Python API ile cagirir, TorchCodec/torchaudio.load kullanmaz.
"""
import os
import sys
import subprocess
import tempfile
import threading
import traceback
import wave
import time
import queue
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

APP_DIR = Path(__file__).resolve().parent
FFMPEG = Path(r"C:\ffmpeg.exe")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EBS AI | Vocal Studio - Ebubekir Bastama")
        self.geometry("850x710")
        self.minsize(440, 470)
        self.configure(fg_color="#141619")
        self.video = None
        self.vocal = None
        self.background = None
        self.is_busy = False
        self.gain_db = ctk.DoubleVar(value=0.0)
        self.playing = False
        self.preview_loading = False
        self.preview_token = 0
        self.play_until = 0.0
        self.preview_file = None
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.events = queue.Queue()
        self.status = ctk.StringVar(value="Video secerek baslayin")
        self.file_label = ctk.StringVar(value="Henuz video secilmedi")
        self._build_ui()
        self.after(100, self._drain_events)

    # METALLIC GREY / GOLD - minimalist responsive layout
    BG = "#141619"
    PANEL = "#25292E"
    PANEL_LIGHT = "#30353A"
    GOLD = "#D9AE59"
    GOLD_HOVER = "#F2CB78"
    MUTED = "#A8ADB1"
    WHITE = "#F4F2EB"

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Scrollable area supports short and narrow screens.
        self.viewport = ctk.CTkScrollableFrame(
            self, fg_color="transparent", corner_radius=0,
            scrollbar_button_color="#55524A",
            scrollbar_button_hover_color=self.GOLD
        )
        self.viewport.grid(row=0, column=0, sticky="nsew")
        self.viewport.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkFrame(self.viewport, fg_color="transparent")
        self.header.grid(row=0, column=0, padx=26, pady=(22, 13), sticky="ew")
        self.header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.header, text="E B S   /   A I   S T U D I O",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=self.GOLD, anchor="w").grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(self.header, text="VOKAL AYIRICI",
                     font=ctk.CTkFont(size=31, weight="bold"),
                     text_color=self.WHITE, anchor="w").grid(row=1, column=0, sticky="ew", pady=(6, 0))
        ctk.CTkLabel(self.header, text="Yapay zekayla ayir  /  Vokali dinle  /  Videoyu kaydet",
                     font=ctk.CTkFont(size=12),
                     text_color=self.MUTED, anchor="w").grid(row=2, column=0, sticky="ew", pady=(0, 10))
        ctk.CTkFrame(self.header, height=2, fg_color=self.GOLD,
                     corner_radius=1).grid(row=3, column=0, sticky="ew")

        panel = ctk.CTkFrame(self.viewport, corner_radius=20,
                             fg_color=self.PANEL, border_width=1,
                             border_color="#555047")
        panel.grid(row=1, column=0, padx=24, pady=(0, 12), sticky="ew")
        panel.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(panel, text="01  /  VIDEO KAYNAGI",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=self.GOLD, anchor="w").grid(
                     row=0, column=0, padx=21, pady=(20, 8), sticky="ew")
        self.filename_widget = ctk.CTkLabel(panel, textvariable=self.file_label,
                     font=ctk.CTkFont(size=12), text_color=self.WHITE,
                     anchor="w", justify="left", wraplength=500)
        self.filename_widget.grid(row=1, column=0, padx=21, pady=(0, 13), sticky="ew")

        self.pick_btn = self._btn(panel, "VIDEO SEC", self.pick_video)
        self.pick_btn.grid(row=2, column=0, padx=21, pady=(0, 10), sticky="ew")
        self.separate_btn = self._btn(panel, "✦   AI ILE VOKALI AYIR", self.start_separate, primary=True)
        self.separate_btn.grid(row=3, column=0, padx=21, pady=(0, 15), sticky="ew")
        self.progress = ctk.CTkProgressBar(panel, mode="indeterminate", height=7,
                     progress_color=self.GOLD, fg_color="#42474B", corner_radius=4)
        self.progress.grid(row=4, column=0, padx=21, pady=(0, 13), sticky="ew")
        self.progress.set(0)
        self.status_widget = ctk.CTkLabel(panel, textvariable=self.status,
                     font=ctk.CTkFont(size=12), text_color=self.MUTED,
                     justify="left", anchor="w", wraplength=500)
        self.status_widget.grid(row=5, column=0, padx=21, pady=(0, 20), sticky="ew")

        edit = ctk.CTkFrame(self.viewport, fg_color=self.PANEL_LIGHT,
                    corner_radius=19, border_width=1, border_color="#555047")
        edit.grid(row=2, column=0, padx=24, pady=(0, 12), sticky="ew")
        edit.grid_columnconfigure(0, weight=1)
        row = ctk.CTkFrame(edit, fg_color="transparent")
        row.grid(row=0, column=0, padx=20, pady=(16, 6), sticky="ew")
        row.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(row, text="02  /  VOKAL SES SEVIYESI",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=self.WHITE, anchor="w").grid(row=0, column=0, sticky="w")
        self.gain_label = ctk.CTkLabel(row, text="+0 dB",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=self.GOLD)
        self.gain_label.grid(row=0, column=1, sticky="e", padx=(8, 0))
        self.gain_slider = ctk.CTkSlider(edit, from_=-12, to=18, number_of_steps=30,
                     variable=self.gain_db, command=self._on_gain_change,
                     fg_color="#555B5F", progress_color=self.GOLD,
                     button_color="#F4D595", button_hover_color="#FFF0BA")
        self.gain_slider.grid(row=1, column=0, padx=24, pady=(10, 10), sticky="ew")
        ctk.CTkLabel(edit, text="-12 dB  —  +18 dB     |     Onizleme ve videoya ayni ayar uygulanir",
                     text_color=self.MUTED, font=ctk.CTkFont(size=11)).grid(
                     row=2, column=0, padx=10, pady=(0, 18))

        controls = ctk.CTkFrame(self.viewport, fg_color="transparent")
        controls.grid(row=3, column=0, padx=24, pady=(0, 9), sticky="ew")
        controls.grid_columnconfigure(0, weight=1)
        controls.grid_columnconfigure(1, weight=1)
        self.listen_btn = self._btn(controls, "VOKALI DINLE", self.listen)
        self.listen_btn.grid(row=0, column=0, padx=(0, 6), pady=3, sticky="ew")
        self.save_btn = self._btn(controls, "VOKALLI VIDEOYU KAYDET", self.start_export, primary=True)
        self.save_btn.grid(row=0, column=1, padx=(6, 0), pady=3, sticky="ew")
        self.listen_btn.configure(state="disabled")
        self.save_btn.configure(state="disabled")

        footer = ctk.CTkFrame(self.viewport, fg_color="transparent")
        footer.grid(row=4, column=0, padx=24, pady=(8, 22), sticky="ew")
        footer.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(footer, text="EBS AI STUDIO   •   Yazilimci: Ebubekir Bastama",
                     text_color=self.GOLD, font=ctk.CTkFont(size=12, weight="bold")).grid(
                     row=0, column=0, sticky="ew")
        ctk.CTkLabel(footer, text="C:\\ffmpeg.exe  •  Ilk ayrimda AI modeli indirilir  •  Orijinal video korunur",
                     text_color=self.MUTED, font=ctk.CTkFont(size=10)).grid(
                     row=1, column=0, sticky="ew", pady=(4, 0))

        self._layout_mode = None
        self.bind("<Configure>", self._on_resize)
        self.after(200, self._adapt_width)

    def _on_resize(self, event):
        if event.widget is self:
            self._adapt_width()

    def _adapt_width(self):
        # Two buttons side-by-side on roomy windows; stacked on narrow windows.
        width = self.winfo_width()
        mode = "narrow" if width < 650 else "wide"
        if mode != self._layout_mode:
            self._layout_mode = mode
            self.listen_btn.grid_forget()
            self.save_btn.grid_forget()
            if mode == "narrow":
                self.listen_btn.grid(row=0, column=0, columnspan=2, padx=0, pady=(0, 8), sticky="ew")
                self.save_btn.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky="ew")
            else:
                self.listen_btn.grid(row=0, column=0, padx=(0, 6), pady=3, sticky="ew")
                self.save_btn.grid(row=0, column=1, padx=(6, 0), pady=3, sticky="ew")
        wrap = max(245, min(680, width - 115))
        self.filename_widget.configure(wraplength=wrap)
        self.status_widget.configure(wraplength=wrap)

    def _btn(self, parent, text, command, primary=False):
        return ctk.CTkButton(
            parent, text=text, command=command, height=49,
            corner_radius=12, border_width=1,
            border_color="#EDC87C" if primary else "#656667",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=self.GOLD if primary else "#41464C",
            hover_color=self.GOLD_HOVER if primary else "#626365",
            text_color="#191919" if primary else self.WHITE
        )

    def pick_video(self):
        path = filedialog.askopenfilename(title="Video sec", filetypes=[
            ("Video dosyalari", "*.mp4 *.mov *.mkv *.avi *.m4v *.webm"), ("Tum dosyalar", "*.*")])
        if path:
            self._stop_preview()
            self.video = Path(path)
            self.vocal = None
            self.background = None
            self.file_label.set(self.video.name)
            self.status.set("Hazir. Yapay zeka ile ayir dugmesine basin.")
            self.listen_btn.configure(state="disabled")
            self.save_btn.configure(state="disabled")

    def _set_busy(self, busy):
        self.is_busy = busy
        if busy:
            self._stop_preview()
        self.gain_slider.configure(state="disabled" if busy else "normal")
        self.pick_btn.configure(state="disabled" if busy else "normal")
        self.separate_btn.configure(state="disabled" if busy else "normal")
        self.listen_btn.configure(state="disabled" if busy or self.vocal is None else "normal")
        self.save_btn.configure(state="disabled" if busy or self.vocal is None else "normal")
        if busy:
            self.progress.start()
        else:
            self.progress.stop()
            self.progress.set(0)

    def _run_ffmpeg(self, arguments):
        if not FFMPEG.is_file():
            raise FileNotFoundError("FFmpeg bulunamadi: C:\\ffmpeg.exe")
        kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE, "text": True,
                  "encoding": "utf-8", "errors": "replace"}
        if os.name == "nt":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        result = subprocess.run([str(FFMPEG), "-hide_banner", "-loglevel", "error", "-y", *arguments], **kwargs)
        if result.returncode:
            raise RuntimeError("FFmpeg hatasi:\n" + result.stderr[-1800:])

    def _notify(self, kind, value):
        self.events.put((kind, value))

    def _drain_events(self):
        try:
            while True:
                kind, value = self.events.get_nowait()
                if kind == "status":
                    self.status.set(value)
                elif kind == "done":
                    self._set_busy(False)
                    self.status.set("Vokal hazir! Dinleyin; begendiyseniz video olarak kaydedin.")
                elif kind == "preview_ready":
                    token, preview_path = value
                    if token == self.preview_token and not self.is_busy and self.vocal is not None:
                        self.preview_loading = False
                        self._start_playback(preview_path)
                elif kind == "preview_error":
                    token, error = value
                    if token == self.preview_token:
                        self._stop_preview()
                        messagebox.showerror("Onizleme hatasi", error)
                elif kind == "exported":
                    self._set_busy(False)
                    self.status.set("Video kaydedildi.")
                    messagebox.showinfo("Tamamlandi", f"Yeni video olusturuldu:\n{value}")
                elif kind == "error":
                    self._set_busy(False)
                    self.status.set("Islem tamamlanamadi")
                    messagebox.showerror("Hata", value)
        except queue.Empty:
            pass
        self.after(100, self._drain_events)

    def start_separate(self):
        if self.is_busy:
            return
        if not self.video:
            messagebox.showwarning("Video gerekli", "Once video secin.")
            return
        self._stop_preview()
        self.vocal = None
        self.background = None
        self._set_busy(True)
        threading.Thread(target=self._separate, args=(self.video,), daemon=True).start()

    def _separate(self, video):
        try:
            import numpy as np
            import soundfile as sf
            import torch
            from demucs.pretrained import get_model
            from demucs.apply import apply_model

            self._notify("status", "Videodan ses cikariliyor...")
            # Her islem farkli dosyaya kaydedilir, kayitlar karismaz.
            out_folder = video.parent / (video.stem + "_EBS_AI")
            out_folder.mkdir(parents=True, exist_ok=True)
            original_wav = out_folder / "_gecici_orijinal.wav"
            self._run_ffmpeg(["-i", str(video), "-vn", "-ac", "2", "-ar", "44100",
                              "-c:a", "pcm_s16le", str(original_wav)])

            self._notify("status", "Yapay zeka modeli yukleniyor (ilk kullanimda internet gerekir)...")
            model = get_model("htdemucs")
            model.eval()
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self._notify("status", "AI sesleri ayiriyor... CPU kullaniliyorsa biraz surebilir.")
            audio, sample_rate = sf.read(str(original_wav), dtype="float32", always_2d=True)
            if int(sample_rate) != 44100:
                raise RuntimeError("Ses ornekleme hizi beklenenden farkli.")
            mix = torch.from_numpy(audio.T.copy())
            ref = mix.mean(dim=0)
            mean = ref.mean()
            std = ref.std().clamp(min=1e-8)
            normalized = (mix - mean) / std
            with torch.no_grad():
                stems = apply_model(model, normalized.unsqueeze(0), device=device,
                                    split=True, shifts=0, overlap=0.25, progress=False)[0]
            vocal_idx = model.sources.index("vocals")
            voice = (stems[vocal_idx] * std + mean).cpu().numpy().T
            # Ayrilmis vokalin kalan kismi dip ses / muzik olarak tutulur.
            residual = audio[:len(voice)] - voice
            vocal_path = out_folder / "VOKAL.wav"
            background_path = out_folder / "DIP_SES.wav"
            # Limit kesmeye karsi; ses seviyesi degistirilmez, sadece fazla tepe varsa normalize edilir.
            voice_peak = float(np.max(np.abs(voice))) if voice.size else 0.0
            if voice_peak > 0.99:
                voice *= 0.99 / voice_peak
            sf.write(str(vocal_path), voice, 44100, subtype="PCM_16")
            sf.write(str(background_path), np.clip(residual, -1, 1), 44100, subtype="PCM_16")
            self.vocal = vocal_path
            self.background = background_path
            try:
                original_wav.unlink()
            except OSError:
                pass
            self._notify("done", str(vocal_path))
        except Exception as exc:
            self._notify("error", f"{exc}\n\nAyrintilar:\n{traceback.format_exc()[-2500:]}")

    def _on_gain_change(self, value):
        self.gain_label.configure(text=f"{int(round(value)):+d} dB")
        # Dinlenen sesin seviyesi degistiginde eskisini durduruyoruz.
        if self.playing or self.preview_loading:
            self._stop_preview()

    def _stop_preview(self):
        self.preview_token += 1
        self.preview_loading = False
        self.playing = False
        if sys.platform == "win32":
            try:
                import winsound
                winsound.PlaySound(None, 0)
            except RuntimeError:
                pass
        if hasattr(self, "listen_btn"):
            self.listen_btn.configure(text="VOKALI DINLE")

    @staticmethod
    def _gain_filter(db):
        # alimiter asiri tepe seviyelerinde sert clipping olusmasini onler.
        # level=0 otomatik telafi kazancini kapatir.
        return f"volume={db:+.0f}dB,alimiter=limit=0.95:level=0"

    def _preview_worker(self, token, gain, source, destination):
        try:
            self._run_ffmpeg(["-i", str(source), "-af", self._gain_filter(gain),
                              "-c:a", "pcm_s16le", str(destination)])
            self._notify("preview_ready", (token, destination))
        except Exception as exc:
            self._notify("preview_error", (token, str(exc)))

    def _start_playback(self, path):
        if sys.platform != "win32":
            self.status.set(f"Dinleme dosyasi: {path}")
            return
        try:
            import winsound
            with wave.open(str(path), "rb") as wav:
                seconds = wav.getnframes() / wav.getframerate()
            winsound.PlaySound(str(path), winsound.SND_FILENAME | winsound.SND_ASYNC)
            self.playing = True
            self.play_until = time.monotonic() + seconds
            self.listen_btn.configure(text="DINLEMEYI DURDUR")
            self.status.set("Vokal caliyor. Ayni dugmeye basarak durdurabilirsiniz.")
            self.after(250, self._check_playback)
        except Exception as exc:
            self._stop_preview()
            messagebox.showerror("Oynatma hatasi", str(exc))

    def _check_playback(self):
        if not self.playing:
            return
        if time.monotonic() >= self.play_until:
            self._stop_preview()
            self.status.set("Dinleme sona erdi.")
        else:
            self.after(250, self._check_playback)

    def listen(self):
        if self.playing or self.preview_loading:
            self._stop_preview()
            self.status.set("Dinleme durduruldu.")
            return
        if not self.vocal or not self.vocal.exists() or self.is_busy:
            return
        if sys.platform != "win32":
            messagebox.showinfo("Bilgi", "Bu oynatici Windows icin hazirlandi.")
            return
        self.preview_token += 1
        token = self.preview_token
        self.preview_loading = True
        self.listen_btn.configure(text="HAZIRLAMAYI DURDUR")
        self.status.set("Ayarladiginiz ses seviyesiyle onizleme hazirlaniyor...")
        # Her tiklamada farkli dosya: iptal edilen is dosyayi bozamaz.
        preview = self.vocal.parent / f"_VOKAL_ONIZLEME_{token}.wav"
        self.preview_file = preview
        threading.Thread(target=self._preview_worker,
                         args=(token, int(round(self.gain_db.get())), self.vocal, preview),
                         daemon=True).start()

    def _on_close(self):
        self._stop_preview()
        self.destroy()

    def start_export(self):
        if self.is_busy or not self.video or not self.vocal:
            return
        target = filedialog.asksaveasfilename(title="Yalniz vokalli videoyu kaydet",
                                              defaultextension=".mp4", filetypes=[("MP4", "*.mp4")],
                                              initialfile=self.video.stem + "_EBS_SADECE_VOKAL.mp4",
                                              initialdir=str(self.video.parent))
        if not target:
            return
        if Path(target).resolve() == self.video.resolve():
            messagebox.showerror("Hata", "Orijinal video uzerine kayit yapilamaz.")
            return
        self._set_busy(True)
        gain = int(round(self.gain_db.get()))
        threading.Thread(target=self._export, args=(Path(target), gain), daemon=True).start()

    def _export(self, target, gain):
        try:
            self._notify("status", "Vokalli yeni video kaydediliyor...")
            # Dinlerken kullanilan ses yuksekligi ve limiter aynen videoya uygulanir.
            self._run_ffmpeg(["-i", str(self.video), "-i", str(self.vocal),
                              "-filter_complex", f"[1:a]{self._gain_filter(gain)}[vokal]",
                              "-map", "0:v:0", "-map", "[vokal]", "-c:v", "copy",
                              "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart",
                              str(target)])
            self._notify("exported", str(target))
        except Exception as exc:
            self._notify("error", str(exc))


if __name__ == "__main__":
    App().mainloop()
