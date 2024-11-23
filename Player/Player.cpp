#include <iostream>
#include <windows.h>
#include <vector>
#include <chrono>
#include <thread>
#include <fstream>
#include <iomanip>
#include <optional>
#include "json.hpp"
#include "argparse.hpp"

using json = nlohmann::json;

class MusicNote {
public:
    int note;
    double duration;
    double position;

    MusicNote(int note, double duration, double position)
        : note(note), duration(duration), position(position) {}

    static MusicNote from_json(const json& j) {
        return MusicNote(j.at("note").get<int>(), j.at("duration").get<double>(), j.at("position").get<double>());
    }
};

void pressKey(WORD key) {
    INPUT input = { 0 };
    input.type = INPUT_KEYBOARD;
    input.ki.wVk = key;
    SendInput(1, &input, sizeof(INPUT));
    std::this_thread::sleep_for(std::chrono::milliseconds(5));

    // Release the key
    input.ki.dwFlags = KEYEVENTF_KEYUP;
    SendInput(1, &input, sizeof(INPUT));
    std::this_thread::sleep_for(std::chrono::milliseconds(5));
}

void pressNote(int note) {
    if (note >= 40 && note < 49) {
        WORD section_key = '0' + (note - 39);
        pressKey(section_key);
        pressKey('Q');
    } else if (note >= 49 && note < 58) {
        WORD section_key = '0' + (note - 48);
        pressKey(section_key);
        pressKey('W');
    } else if (note >= 58 && note < 66) {
        WORD section_key = '0' + (note - 57);
        pressKey(section_key);
        pressKey('E');
    } else if (note >= 66 && note < 71) {
        WORD section_key = '0' + (note - 65);
        pressKey(section_key);
        pressKey('R');
    } else if (note >= 71 && note < 75) {
        WORD section_key = '0' + (note - 70);
        pressKey(section_key);
        pressKey('T');
    }
}

double getCurrentTime()
{
    return std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::system_clock::now().time_since_epoch()).count() / 1e9;
}

void playTrack(const std::string& filename, const std::string& track_name, double tempo_factor = 1.0, int note_shift = 0)
{
    std::ifstream file(filename);
    json j;
    file >> j;

    auto notes_json = j.at("tracks").at(track_name).at("notes");

    std::vector<MusicNote> notes;
    for (const auto& note : notes_json)
    {
        auto note_obj = MusicNote::from_json(note);
        note_obj.position /= tempo_factor;
        note_obj.duration /= tempo_factor;
        notes.push_back(note_obj);
    }

    //Print number of notes
    std::cout << "Number of notes: " << notes.size() << std::endl;

    //Sort notes by position
    std::sort(notes.begin(), notes.end(), [](const MusicNote& a, const MusicNote& b)
    {
        return a.position < b.position;
    });

    double start_time = getCurrentTime();
    for(int i = 0; i < notes.size(); i++)
    {
        std::cout << "Playing note " << i << " at position " << std::fixed << std::setw(8) << std::setprecision(4) << notes[i].position << " with pitch " << notes[i].note + note_shift << std::endl;
        pressNote(notes[i].note + note_shift);

        if(i < notes.size() - 1)
        {
            double next_note_time = start_time + notes[i + 1].position;
            double current_time = getCurrentTime();
            double sleep_time = next_note_time - current_time;
            if(sleep_time > 0)
            {
                std::this_thread::sleep_for(std::chrono::milliseconds((int)(sleep_time * 1000)));
            }
        }
    }


}

struct ProgramArguements
{
    double start_delay;
    double tempo_factor;
    std::string input_file_path;
    std::string track_name;
    int note_shift;
};

std::optional<ProgramArguements> processArguments(int argc, char* argv[])
{
    argparse::ArgumentParser arguments("player.exe", "1.0", argparse::default_arguments::none);
    arguments.add_argument("-d", "--delay")
        .help("Delay before playing the song in seconds")
        .default_value(5.0)
        .scan<'g', double>();
    arguments.add_argument("-i", "--input_file")
        .help("Input file path")
        .required();
    arguments.add_argument("-t", "--track")
        .help("Track name")
        .required();
    arguments.add_argument("-f", "--tempo_factor")
        .help("Tempo factor")
        .default_value(1.0)
        .scan<'g', double>();
    arguments.add_argument("-s", "--note_shift")
        .help("Shifts the notes played by this amount")
        .default_value(0)
        .scan<'i', int>();

    try
    {
        arguments.parse_args(argc, argv);
    }
    catch (const std::runtime_error& err)
    {
        std::cerr << err.what() << std::endl;
        std::cerr << arguments;
        return std::nullopt;
    }

    ProgramArguements program_arguements;
    program_arguements.start_delay = arguments.get<double>("-d");
    program_arguements.input_file_path = arguments.get<std::string>("-i");
    program_arguements.track_name = arguments.get<std::string>("-t");
    program_arguements.tempo_factor = arguments.get<double>("-f");
    program_arguements.note_shift = arguments.get<int>("-s");

    if (program_arguements.tempo_factor <= 0)
    {
        std::cerr << "Tempo factor must be greater than 0" << std::endl;
        return std::nullopt;
    }

    return program_arguements;
}


int main(int argc, char* argv[])
{
    auto arguemnts = processArguments(argc, argv);

    if(!arguemnts)
    {
        return -1;
    }

    std::this_thread::sleep_for(std::chrono::milliseconds((int)(arguemnts->start_delay * 1000)));
    std::cout << "Playing " << arguemnts->input_file_path << " (" <<  arguemnts->track_name << ") with tempo factor " << arguemnts->tempo_factor <<
        " and a note shift of " << arguemnts->note_shift << std::endl;
    playTrack(
        arguemnts->input_file_path,
        arguemnts->track_name,
        arguemnts->tempo_factor,
        arguemnts->note_shift
    );
    return 0;
}