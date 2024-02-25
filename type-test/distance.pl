#!/usr/bin/perl
use strict;
use warnings;

sub trim {
    my $s = shift;
    $s =~ s/^\s+|\s+$//g; # Remove leading and trailing whitespace
    return $s;
}

sub levenshtein_distance {
    my ($s1, $s2) = @_;

    my $len1 = length $s1;
    my $len2 = length $s2;
    my @matrix;

    for my $i (0 .. $len1) {
        $matrix[$i][0] = $i;
    }

    for my $j (0 .. $len2) {
        $matrix[0][$j] = $j;
    }

    for my $i (1 .. $len1) {
        for my $j (1 .. $len2) {
            my $cost = (substr($s1, $i-1, 1) eq substr($s2, $j-1, 1)) ? 0 : 1;
            $matrix[$i][$j] = min(
                $matrix[$i-1][$j] + 1,    # Deletion
                $matrix[$i][$j-1] + 1,    # Insertion
                $matrix[$i-1][$j-1] + $cost # Substitution
            );
        }
    }

    return $matrix[$len1][$len2];
}

sub min {
    my ($x, $y, $z) = @_;
    if ($x < $y) {
        return $x < $z ? $x : $z;
    } else {
        return $y < $z ? $y : $z;
    }
}

sub calculate_similarity {
    my ($s1, $s2) = @_;
    my $distance = levenshtein_distance($s1, $s2);
    my $max_len = length($s1) > length($s2) ? length($s1) : length($s2);
    my $similarity = (($max_len - $distance) / $max_len) * 100;
    return $similarity;
}

sub calculate_true_wpm {
    my ($raw_wpm, $accuracy) = @_;
    return $raw_wpm * ($accuracy / 100);
}


if (@ARGV != 4) {
    die "Usage: $0 string1 string2 raw_wpm num_chars\n";
}

my ($str1, $str2, $raw_wpm, $num_chars) = @ARGV;
# trim whitespace off ends
$str1 = trim($str1);
$str2 = trim($str2);

my $similarity = calculate_similarity($str1, $str2);
my $true_wpm = calculate_true_wpm($raw_wpm, $similarity);

printf("Similarity: %.2f%%\n", $similarity);
printf("True WPM: %.2f\n", $true_wpm);

