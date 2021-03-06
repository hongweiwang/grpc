#region Copyright notice and license

// Copyright 2015, Google Inc.
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//     * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
//     * Neither the name of Google Inc. nor the names of its
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#endregion

using System;
using System.Threading;

namespace Grpc.Core.Internal
{
    internal class DebugStats
    {
        public readonly AtomicCounter ActiveClientCalls = new AtomicCounter();

        public readonly AtomicCounter ActiveServerCalls = new AtomicCounter();

        public readonly AtomicCounter PendingBatchCompletions = new AtomicCounter();

        /// <summary>
        /// Checks the debug stats and take action for any inconsistency found.
        /// </summary>
        public void CheckOK()
        {
            var remainingClientCalls = ActiveClientCalls.Count;
            if (remainingClientCalls != 0)
            {                
                DebugWarning(string.Format("Detected {0} client calls that weren't disposed properly.", remainingClientCalls));
            }
            var remainingServerCalls = ActiveServerCalls.Count;
            if (remainingServerCalls != 0)
            {
                DebugWarning(string.Format("Detected {0} server calls that weren't disposed properly.", remainingServerCalls));
            }
            var pendingBatchCompletions = PendingBatchCompletions.Count;
            if (pendingBatchCompletions != 0)
            {
                DebugWarning(string.Format("Detected {0} pending batch completions.", pendingBatchCompletions));
            }
        }

        private void DebugWarning(string message)
        {
            throw new Exception("Shutdown check: " + message);
        }
    }
}
