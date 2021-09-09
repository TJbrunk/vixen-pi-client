using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace VixenClient {
    public class ClientConfig {
        public ushort Universe { get; set; }
        public List<Channel> Channels { get; set; }
    }

    public class Channel {
        public string Name { get; set; }
        public int StartIndex { get; set; }
        public int Pin { get; set; }
        public bool IsRGB { get; set; }
        public int PixelCount { get; set; }
    }
}
