import subprocess

class AudioManager:
    def __init__(self, tracks: dict[str, str]):
        self.tracks = tracks
        self.current = None  # Popen

    def play(self, key: str, loop: bool = False):
        self.stop()
        cmd = ["mpg123", "-q"]
        if loop:
            cmd += ["--loop", "-1"]
        cmd.append(self.tracks[key])
        self.current = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def stop(self):
        if self.current and self.current.poll() is None:
            self.current.terminate()
            self.current.wait()
        self.current = None