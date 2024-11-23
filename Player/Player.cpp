#include <iostream>
#include <windows.h>
#include <vector>
#include <chrono>
#include <thread>
#include <fstream>
#include <iomanip>
#include "json.hpp"

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

void playTrack(const std::string& filename, const std::string& track_name)
{
    std::ifstream file(filename);
    json j;
    file >> j;

    auto notes_json = j.at("tracks").at(track_name).at("notes");

    std::vector<MusicNote> notes;
    for (const auto& note : notes_json)
    {
        notes.push_back(MusicNote::from_json(note));
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
        std::cout << "Playing note " << i << " at position " << std::fixed << std::setw(8) << std::setprecision(4) << notes[i].position << " with pitch " << notes[i].note << std::endl;
        pressNote(notes[i].note - 24);

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

int main()
{
    std::this_thread::sleep_for(std::chrono::seconds(5));
    const std::string filename = "./ConvertedSongs/bike2.json";
    std::cout << "Playing " << filename << std::endl;
    playTrack(filename, "Track 2");
    return 0;
}