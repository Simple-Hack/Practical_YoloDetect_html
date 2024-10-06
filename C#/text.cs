using System;

namespace UnitTestDemo
{
    public class Score
    {
        public static char TestMe(float score)
        {
            if(score<0 || score > 100)
            {
                throw new ArgumentOutOfRangeException();
            }
            if (score >= 90)
            {
                return 'A';
            }
            else if (score >= 80)
            {
                return 'B';
            }
            else if (score >= 70)
            {
                return 'C';
            }
            else if (score >= 60)
            {
                return 'D';
            }
            else
            {
                return 'E';
            }
        }
    }
}