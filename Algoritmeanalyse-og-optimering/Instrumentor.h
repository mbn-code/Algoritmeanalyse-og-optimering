//
// Basic instrumentation profiler by Cherno

// Usage: include this header file somewhere in your code (eg. precompiled header), and then use like:
//
// Instrumentor::Get().BeginSession("Session Name");        // Begin session 
// {
//     InstrumentationTimer timer("Profiled Scope Name");   // Place code like this in scopes you'd like to include in profiling
//     // Code
// }
// Instrumentor::Get().EndSession();                        // End Session
//
// You will probably want to macro-fy this, to switch on/off easily and use things like __FUNCSIG__ for the profile name.
//
#pragma once

#include <string>
#include <chrono>
#include <algorithm>
#include <fstream>

#include <thread>

struct ProfileResult
{
    std::string Name;
    long long Start, End;
    uint32_t ThreadID;
	std::string Category;
};

struct InstrumentationSession
{
    std::string Name;
};

class Instrumentor
{
private:
    InstrumentationSession* m_CurrentSession;
    std::ofstream m_OutputStream;
    int m_ProfileCount;
    std::vector<ProfileResult> m_Results; // Store all profiling results

public:
    static Instrumentor& Get()
    {
        static Instrumentor instance;
        return instance;
    }

    void BeginSession(const std::string& name, const std::string& filepath = "results.json")
    {
        m_OutputStream.open(filepath);
        WriteHeader();
        m_CurrentSession = new InstrumentationSession{ name };
        m_ProfileCount = 0;
    }

    void EndSession()
    {
        WriteFooter();
        m_OutputStream.close();
        delete m_CurrentSession;
        m_CurrentSession = nullptr;
    }

    void WriteProfile(const ProfileResult& result)
    {
        if (m_ProfileCount++ > 0)
            m_OutputStream << ",";

        std::string name = result.Name;
        std::replace(name.begin(), name.end(), '"', '\'');

        std::cout << "Writing profile: " << result.Name << std::endl; // Debugging print

        m_OutputStream << "{";
        m_OutputStream << "\"cat\":\"" << result.Category << "\",";
        m_OutputStream << "\"dur\":" << (result.End - result.Start) << ',';
        m_OutputStream << "\"name\":\"" << name << "\",";
        m_OutputStream << "\"ph\":\"X\",";
        m_OutputStream << "\"pid\":0,";
        m_OutputStream << "\"tid\":" << result.ThreadID << ",";
        m_OutputStream << "\"ts\":" << result.Start;
        m_OutputStream << "}";
    }


    void WriteHeader()
    {
        m_OutputStream << "{\"otherData\": {},\"traceEvents\":[";
        m_OutputStream.flush();
    }

    void WriteFooter()
    {
        m_OutputStream << "]}";
        m_OutputStream.flush();
    }

    void AddResult(const ProfileResult& result)
    {
        m_Results.push_back(result);
    }

    const std::vector<ProfileResult>& GetResults() const
    {
        return m_Results;
    }
};

class InstrumentationTimer
{
public:
    InstrumentationTimer(const char* name, const char* category)
        : m_Name(name), m_Stopped(false), m_Category(category)
    {
        m_StartTimepoint = std::chrono::high_resolution_clock::now();
    }

    ~InstrumentationTimer()
    {
        if (!m_Stopped)
            Stop();
    }

    void Stop() {
        auto endTimepoint = std::chrono::high_resolution_clock::now();

        auto start = std::chrono::time_point_cast<std::chrono::microseconds>(m_StartTimepoint).time_since_epoch();
        auto end = std::chrono::time_point_cast<std::chrono::microseconds>(endTimepoint).time_since_epoch();

        long long duration = std::chrono::duration_cast<std::chrono::microseconds>(endTimepoint - m_StartTimepoint).count();

        uint32_t threadID = std::hash<std::thread::id>{}(std::this_thread::get_id());
        ProfileResult result = { m_Name, start.count(), end.count(), threadID, m_Category };
        Instrumentor::Get().WriteProfile(result);
        Instrumentor::Get().AddResult(result);

        m_Stopped = true;
    }

private:
    const char* m_Name;
    std::chrono::time_point<std::chrono::high_resolution_clock> m_StartTimepoint;
    bool m_Stopped;
    const char* m_Category;
};



void SaveProfilingData(const std::string& filepath)
{
    std::ofstream file(filepath);
    if (file.is_open())
    {
        file << "{\"otherData\": {},\"traceEvents\":[";

        const auto& results = Instrumentor::Get().GetResults();
        if (results.empty()) {
            std::cout << "No profiling data recorded!" << std::endl;
        }

        for (size_t i = 0; i < results.size(); ++i)
        {
            const auto& result = results[i];
            if (i > 0)
                file << ",";

            file << "{";
            file << "\"cat\":\"" << result.Category << "\",";
            file << "\"dur\":" << (result.End - result.Start) << ',';
            file << "\"name\":\"" << result.Name << "\",";
            file << "\"ph\":\"X\",";
            file << "\"pid\":0,";
            file << "\"tid\":" << result.ThreadID << ",";
            file << "\"ts\":" << result.Start << ",";
            file << "\"start_time\":\"" << std::chrono::system_clock::to_time_t(std::chrono::system_clock::now() + std::chrono::microseconds(result.Start)) << "\",";
            file << "\"end_time\":\"" << std::chrono::system_clock::to_time_t(std::chrono::system_clock::now() + std::chrono::microseconds(result.End)) << "\"";
            file << "}";
        }

        file << "]}";
        file.close();
    }
    else {
        std::cout << "Failed to open file for profiling data!" << std::endl;
    }
}

