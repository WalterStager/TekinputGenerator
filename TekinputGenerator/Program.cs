using ImGuiWindower;
using ImGuiNET;

class ProgramWindow : ImGuiWindow
{
    public ProgramWindow(string windowName) : base(windowName) { }

    public override void SubmitUI()
    {
        ImGui.Text("SampleText");
    }
}

class Program
{
    public static void Main(string[] args)
    {
        ProgramWindow pw = new ProgramWindow("TekInputGenerator");

        pw.mainloop();
    }
}